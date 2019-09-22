import subprocess as sp
import os
import time


class Camera:
    def __init__(self, name, uri):
        self.name = name
        self.uri = uri

    def __str__(self):
        return self.name + " (" + self.uri + ")"

    def __repr__(self):
        return self.__str__()


class CameraSnapshot:
    image_compression = 10
    
    def __init__(self, ffmpeg_bin, snapshots_dir):
        self.__ffmpeg_bin = ffmpeg_bin
        self.__snapshots_dir = snapshots_dir
        self.__create_folder_if_needed(snapshots_dir)

    def __create_folder_if_needed(self, folder_path):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print("Created folder", folder_path)

    def __get_path(self, *path_elements):
        return "/".join(list(filter(lambda x: x != "", path_elements)))

    # take jpeg snapshot from camera
    def take_video_snapshot(self, camera):
        self.__create_folder_if_needed(self.__get_path(self.__snapshots_dir, camera.name))

        print("Snapshot for camera", camera, "at", int(time.time()))
        ffmpeg_cmd = [self.__ffmpeg_bin,
                      '-i', camera.uri,
                      '-f', 'image2',
                      '-loglevel', 'error',
                      '-vframes', '1',
                      '-strftime', '1',
                      '-qscale:v', str(self.image_compression),
                      self.__get_path(self.__snapshots_dir, camera.name, camera.name) + '_%s.jpg']
        sp.run(ffmpeg_cmd)
