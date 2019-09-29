import yaml
import os

import logger


def _override_with_env_variables(props, prefix=""):
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


def get_properties(yaml_file):
    with open(yaml_file) as yaml_file_handler:
        config = yaml.load(yaml_file_handler, yaml.Loader)
    _override_with_env_variables(config)
    return config
