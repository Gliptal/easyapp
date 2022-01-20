import logging
import logging.config
from pathlib import Path

from ruamel import yaml

import easyapp.exceptions
from easyapp.utils.path import cwd_path


__handlers = {}


def __configure():
    path = Path("config/easyapp")
    name = Path("logging.yml")

    try:
        with cwd_path(path / name).open() as file:
            config = yaml.safe_load(file)
            logging.config.dictConfig(config)
    except FileNotFoundError as error:
        message = f"no config file {name} found in {cwd_path(path)}"
        raise easyapp.exceptions.MissingConfig(message) from error


def debug(active: bool):
    if active:
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)


def suppress(name: str):
    for handler in logging.getLogger().handlers:
        if handler.get_name() == name:
            __handlers[name] = handler
            logging.getLogger().removeHandler(handler)
            break


def recover(name: str):
    logging.getLogger().addHandler(__handlers[name])


__configure()
