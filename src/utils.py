from pathlib import Path

import logging
import yaml


def get_app_base_path():
    return Path(get_app_root_path(), 'src')


def get_app_root_path():
    return Path.cwd()


def load_yaml_config(config_file):
    """ Loads the yaml file
    :param config_file:
    :return:
    """
    config = None
    try:
        with open(config_file, 'r') as file:
            config = yaml.load(file)
    except yaml.YAMLError as exc:
        logging.error(f"Invalid config_file {config_file}: {exc}")
    return config
