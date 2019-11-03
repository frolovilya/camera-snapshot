import yaml
import os
import m3u8

import logger
import webcam


def _override_with_env_variables(props: dict, prefix=""):
    """
    Override properties with system environment variables.
    For example
        props: {
            s3: {
                access_key: None
            }
        }
    can be overridden with S3_ACCESS_KEY variable.

    :param props: properties dictionary
    :param prefix: concatenated parent property keys
    :return: props with overridden values
    """
    for key in props.keys():
        prefixed_key = (key if prefix == "" else prefix + "_" + key).upper()

        if type(props[key]) is dict:
            _override_with_env_variables(props[key], prefixed_key)
        else:
            override = os.getenv(prefixed_key)
            if override is not None:
                logger.log("Override {}={}", prefixed_key, override)
                props[key] = override


def _read_m3u8_cameras_config(playlist_uri: str) -> list:
    """
    Read cameras configuration from remote m3u8 file.

    :param playlist_uri: m3u8 file location
    :return: list of Cameras
    """
    logger.log("Reading cameras configuration from m3u8 playlist {}", playlist_uri)
    playlist = m3u8.load(playlist_uri)
    return [webcam.Camera(s.value, p.uri)
            for p, s in zip(playlist.playlists, playlist.session_data)
            if s.data_id == "camera.name"]


def _init_cameras(props: dict):
    if props["cameras"] is None or len(props["cameras"]) == 0:
        props["cameras"] = _read_m3u8_cameras_config(props['cameras_playlist'])


def get_properties(yaml_file: str) -> dict:
    """
    Read properties from Yaml file.

    :param yaml_file: properties file path
    :return: properties dictionary
    """
    with open(yaml_file) as yaml_file_handler:
        config = yaml.load(yaml_file_handler, yaml.Loader)
    _override_with_env_variables(config)
    _init_cameras(config)
    return config
