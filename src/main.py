from src import webcam, scheduler, storage, config, logger
import pprint

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


def take_snapshots_task():
    for camera in props['cameras']:
        try:
            file_dir, file_name = snap.take_video_snapshot(camera)
            s3_client.upload(file_dir + "/" + file_name, camera.name + "/" + file_name)
        except (webcam.CameraException, storage.StorageException) as e:
            logger.error("{}", e.message)


task_scheduler.schedule_task(take_snapshots_task, props['time_period'])
task_scheduler.start()
