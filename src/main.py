from src import webcam, scheduler, storage, config, logger
import pprint
import datetime

props = config.get_properties("config.yml")

logger.timezone_name = props['logger']['timezone']
logger.log("Loaded properties: \n{}", pprint.pformat(props))

snap = webcam.CameraSnapshot(
    ffmpeg_bin=props['ffmpeg']['bin'],
    jpeg_compression=props['ffmpeg']['jpeg_compression']
)

s3_client = storage.S3Client(
    access_key=props['s3']['access_key'],
    secret_key=props['s3']['secret_key'],
    bucket_name=props['s3']['bucket_name']
)

task_scheduler = scheduler.Scheduler()


def get_target_file_path(camera, timestamp):
    def add_leading_zero(x):
        return str(x) if len(str(x)) > 1 else "0" + str(x)

    date = datetime.datetime.fromtimestamp(timestamp, tz=logger.get_timezone())
    return "{}/{}/{}/{}/{}_{}.jpg".format(camera.name,
                                          date.year, add_leading_zero(date.month), add_leading_zero(date.day),
                                          camera.name, timestamp)


def take_snapshots_task():
    for camera in props['cameras']:
        try:
            source_file_path, timestamp = snap.take_video_snapshot(camera)
            target_file_path = get_target_file_path(camera, timestamp)
            s3_client.upload(source_file_path, target_file_path)
        except (webcam.CameraException, storage.StorageException) as e:
            logger.error("{}", e.message)


task_scheduler.schedule_task(take_snapshots_task, props['time_period'])
task_scheduler.start()
