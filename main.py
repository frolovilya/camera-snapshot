import webcam
import scheduler
import yaml
import pprint


config = yaml.load(open("config.yml"), yaml.Loader)
pprint.pprint(config)
snap = webcam.CameraSnapshot(config['ffmpeg_bin'], config['snapshots_dir'])


def take_snapshots_task():
    for camera in config['cameras']:
        snap.take_video_snapshot(camera)


s = scheduler.Scheduler()
s.schedule_task(take_snapshots_task, config['time_period'])
s.start()
