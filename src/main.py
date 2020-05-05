import datetime
import pprint

import config
import env
import logger
import scheduler
import storage
import webcam


def _get_target_file_path(camera: webcam.Camera, timestamp: float) -> str:
    def add_leading_zero(x):
        return str(x) if len(str(x)) > 1 else "0" + str(x)

    date = datetime.datetime.fromtimestamp(timestamp, tz=env.get_timezone())
    return "{}/{}/{}/{}/{}_{}.jpg".format(camera.folder,
                                          date.year, add_leading_zero(date.month), add_leading_zero(date.day),
                                          camera.name, timestamp)


def _get_s3_client(props: dict) -> storage.S3Client:
    # S3 client is not pickleable thus can't be shared between multiple processes
    return storage.S3Client(
        access_key=props['s3']['access_key'],
        secret_key=props['s3']['secret_key'],
        bucket_name=props['s3']['bucket_name']
    )


def _get_camera_snapshot_taker(props: dict) -> webcam.CameraSnapshot:
    return webcam.CameraSnapshot(
        ffmpeg_bin=props['ffmpeg']['bin'],
        jpeg_compression=int(props['ffmpeg']['jpeg_compression']),
        timeout_sec=int(props['ffmpeg']['timeout_sec'])
    )


def _save_camera_snapshot(camera: webcam.Camera, props: dict):
    """
    Take camera snapshot and upload to S3.
    """
    try:
        source_file_path, timestamp = _get_camera_snapshot_taker(props).take_video_snapshot(camera)
        target_file_path = _get_target_file_path(camera, timestamp)
        _get_s3_client(props).upload(source_file_path, target_file_path)

    except (webcam.CameraException, storage.S3Exception) as e:
        logger.error("{}", e.message)


def run():
    props = config.get_properties("config.yml")
    env.timezone_name = props['env']['timezone']

    logger.start()
    logger.log("Loaded properties: \n{}", pprint.pformat(props))

    task_scheduler = scheduler.Scheduler(int(props['workers']))

    for camera in props['cameras']:
        task_scheduler.add_task(_save_camera_snapshot, camera, props)
    task_scheduler.start(int(props['time_period_sec']))


if __name__ == '__main__':
    run()
