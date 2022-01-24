import logging
import logging.config
from pathlib import Path

from ruamel import yaml

import easyapp.exceptions
import easyapp.utils.path as path


__handlers = {}


def __configure():
    try:
        with path.cwd_path(Path("config/easyapp/logging.yml")).open() as file:
            config = yaml.safe_load(file)

            if path.is_frozen():
                config["handlers"]["file"]["filename"] = "log.log"

            logging.config.dictConfig(config)
    except FileNotFoundError as error:
        raise easyapp.exceptions.MissingConfig from error


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
