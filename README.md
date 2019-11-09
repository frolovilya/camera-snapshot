# camera-snapshot

This service takes web camera snapshots via FFmpeg at a specified time period and uploads them to S3 bucket.


## Usage

The project requires [FFmpeg](https://github.com/FFmpeg/FFmpeg) to be installed. If deploying to Heroku, then this FFmpeg [build pack](https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest) can be used.

All settings are configured in a single [config.yml](https://github.com/frolovilya/camera-snapshot/blob/master/config.yml) file. Check the sources for all available properties and it's descriptions. Minimal setup requires FFmpeg exeutable path, cameras config and S3 credentials, for example:
```
time_period_sec: 3600 # 1 hour

ffmpeg:
  bin: '/usr/bin/ffmpeg'

cameras:
- !!python/object:webcam.Camera
  name: 'Some camera name'
  uri: 'http://video1.example.com/camera.m3u8'
  
s3:
  bucket_name: 'my_camera_photos'
```
It's recommended not to leave your S3 access keys inside config file. All _config.yml_ properties can be overridden via environment variables by joining nested property keys with underscores, for example:
```
export S3_ACCESS_KEY="SOMEACCESSKEY"
export S3_SECRET_KEY="SOMESECRETKEY"
```
Same applies for Config Vars if using Heroku.

# In a picture

![How it works](https://user-images.githubusercontent.com/271293/68529537-c7858d80-0310-11ea-8353-7bd745a23dc9.jpg)
