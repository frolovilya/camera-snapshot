import subprocess as sp
import time
import tempfile

import logger


class Camera:
    def __init__(self, name: str, uri: str):
        self.name = name
        self.uri = uri

    def __str__(self):
        return "{'name': '" + self.name + "', 'uri': '" + self.uri + "'}"

    def __repr__(self):
        return self.__str__()


class CameraException(Exception):
    def __init__(self, message: str):
        self.message = message


class CameraSnapshot:
    def __init__(self, ffmpeg_bin: str, jpeg_compression: int = 5, timeout_sec: int = 300):
        self._ffmpeg_bin = ffmpeg_bin
        self._jpeg_compression = jpeg_compression
        self._timeout_sec = timeout_sec

    def take_video_snapshot(self, camera: Camera, snapshot_dir: str = tempfile.gettempdir()) -> (str, float):
        """
        Take snapshot image from camera.

        :param camera: Camera object
        :param snapshot_dir: snapshot directory to save file to, tempdir by feault
        :return: (snapshot folder, snapshot file name)
        """
        timestamp = int(time.time())
        logger.log("Taking snapshot for camera {} ({})", camera.name, timestamp)

        file_name = camera.name + '_' + str(timestamp) + '.jpg'
        file_path = snapshot_dir + "/" + file_name

        ffmpeg_cmd = [self._ffmpeg_bin,
                      '-i', camera.uri,
                      '-f', 'image2',
                      '-loglevel', 'error',
                      '-vframes', '1',
                      '-qscale:v', str(self._jpeg_compression),
                      file_path]
        try:
            response = sp.run(ffmpeg_cmd, timeout=self._timeout_sec)

            if response.returncode == 0:
                logger.log("Saved snapshot {}", file_path)
            else:
                raise CameraException("Failed to take snapshot for {}. "
                                      "FFMPEG returned non-zero code.".format(camera.name))

        except KeyboardInterrupt as e:
            logger.log("Interrupted FFMPEG while capturing {}", camera.name)
            raise e
        except sp.TimeoutExpired:
            raise CameraException("Timeout occurred while capturing {}".format(camera.name))

        return file_path, timestamp
