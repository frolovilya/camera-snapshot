import subprocess as sp
import time
import tempfile
from src import logger


class Camera:
    def __init__(self, name, uri):
        self.name = name
        self.uri = uri

    def __str__(self):
        return "{'name': '" + self.name + "', 'uri': '" + self.uri + "'}"

    def __repr__(self):
        return self.__str__()


class CameraException(Exception):
    def __init__(self, message):
        self.message = message


class CameraSnapshot:
    def __init__(self, ffmpeg_bin, jpeg_compression=5):
        self._ffmpeg_bin = ffmpeg_bin
        self._jpeg_compression = int(jpeg_compression)

    def take_video_snapshot(self, camera, snapshot_dir=tempfile.gettempdir()):
        """
        Take snapshot image from camera.

        :param camera: Camera object
        :param snapshot_dir: snapshot directory to save file to
        :return: tuple: snapshot folder, snapshot file name
        """
        logger.log("Taking snapshot for camera '{}' ({})", camera.name, int(time.time()))

        file_name = camera.name + '_' + str(int(time.time())) + '.jpg'
        file_path = snapshot_dir + "/" + file_name

        ffmpeg_cmd = [self._ffmpeg_bin,
                      '-i', camera.uri,
                      '-f', 'image2',
                      '-loglevel', 'error',
                      '-vframes', '1',
                      '-qscale:v', str(self._jpeg_compression),
                      file_path]
        response = sp.run(ffmpeg_cmd)

        if response.returncode == 0:
            logger.log("Saved snapshot {} to {}", file_name, file_path)
        else:
            raise CameraException("Failed to take snapshot. FFMPEG returned non-zero code.")

        return snapshot_dir, file_name
