import datetime
import pprint
import multiprocessing as mp

import config
import env
import logger
import scheduler
import storage
import webcam


def get_target_file_path(camera: webcam.Camera, timestamp: float):
    def add_leading_zero(x):
        return str(x) if len(str(x)) > 1 else "0" + str(x)

    date = datetime.datetime.fromtimestamp(timestamp, tz=env.get_timezone())
    return "{}/{}/{}/{}/{}_{}.jpg".format(camera.name,
                                          date.year, add_leading_zero(date.month), add_leading_zero(date.day),
                                          camera.name, timestamp)


class Main:
    def __init__(self):
        self.props = config.get_properties("config.yml")

        env.timezone_name = self.props['env']['timezone']

        logger.start()
        logger.log("Loaded properties: \n{}", pprint.pformat(self.props))

        self.snap = webcam.CameraSnapshot(
            ffmpeg_bin=self.props['ffmpeg']['bin'],
            jpeg_compression=int(self.props['ffmpeg']['jpeg_compression']),
            timeout_sec=int(self.props['ffmpeg']['timeout_sec'])
        )

        self.task_scheduler = scheduler.Scheduler()

    def _init_s3_client(self):
        # S3 client is not pickleable thus can't be shared between multiple processes
        return storage.S3Client(
            access_key=self.props['s3']['access_key'],
            secret_key=self.props['s3']['secret_key'],
            bucket_name=self.props['s3']['bucket_name']
        )

    def _save_camera_snapshot(self, camera: webcam.Camera):
        """
        Take camera snapshot and upload to S3.
        """
        try:
            source_file_path, timestamp = self.snap.take_video_snapshot(camera)
            target_file_path = get_target_file_path(camera, timestamp)
            self._init_s3_client().upload(source_file_path, target_file_path)

        except (webcam.CameraException, storage.S3Exception) as e:
            logger.error("{}", e.message)

    def _async_save_snapshots_task(self):
        """
        Async take camera snapshots in separate worker processes and upload to S3.
        """
        workers = mp.Pool(int(self.props['workers']))

        try:
            for camera in self.props['cameras']:
                workers.apply_async(self._save_camera_snapshot, args=(camera,))

            workers.close()
            workers.join()
            logger.log("Finished tasks")

        except KeyboardInterrupt as e:
            workers.terminate()
            logger.log("Interrupted workers pool")
            raise e

    def run(self):
        self.task_scheduler.schedule_task(self._async_save_snapshots_task, int(self.props['time_period_sec']))
        self.task_scheduler.start()


if __name__ == '__main__':
    Main().run()
