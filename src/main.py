import datetime
import pprint

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


def run():
    props = config.get_properties("config.yml")

    env.timezone_name = props['env']['timezone']

    logger.log("Loaded properties: \n{}", pprint.pformat(props))

    snap = webcam.CameraSnapshot(
        ffmpeg_bin=props['ffmpeg']['bin'],
        jpeg_compression=int(props['ffmpeg']['jpeg_compression'])
    )

    s3_client = storage.S3Client(
        access_key=props['s3']['access_key'],
        secret_key=props['s3']['secret_key'],
        bucket_name=props['s3']['bucket_name']
    )

    task_scheduler = scheduler.Scheduler()

    def take_snapshots_task():
        for camera in props['cameras']:
            try:
                source_file_path, timestamp = snap.take_video_snapshot(camera)
                target_file_path = get_target_file_path(camera, timestamp)
                s3_client.upload(source_file_path, target_file_path)
            except (webcam.CameraException, storage.StorageException) as e:
                logger.error("{}", e.message)

    task_scheduler.schedule_task(take_snapshots_task, int(props['time_period']))
    task_scheduler.start()


if __name__ == '__main__':
    run()
