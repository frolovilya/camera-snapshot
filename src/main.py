from src import webcam, scheduler, storage, config, logger
import pprint

props = config.get_properties("config.yml")
logger.log("Loaded properties: {}", pprint.pformat(props))

snap = webcam.CameraSnapshot(
    ffmpeg_bin=props['ffmpeg']['bin'],
    jpeg_compression=props['ffmpeg']['jpeg_compression']
)

s3 = storage.S3Client(
    access_key=props['s3']['access_key'],
    secret_key=props['s3']['secret_key'],
    bucket_name=props['s3']['bucket_name']
)

s = scheduler.Scheduler()


def take_snapshots_task():
    for camera in props['cameras']:
        file_dir, file_name = snap.take_video_snapshot(camera)
        #s3.upload(file_dir + "/" + file_name, camera.name + "/" + file_name)


s.schedule_task(take_snapshots_task, props['time_period'])
s.start()
