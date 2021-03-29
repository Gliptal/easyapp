import logging
import logging.config

from ruamel import yaml

import easyapp.utils.path as path


class LogManager:

    FILEPATH = path.cwd_path("config/easyapp/logging.yml")

    def __init__(self):
        self.__configure()

    @property
    def debug(self) -> bool:
        return self.__debug

    @debug.setter
    def debug(self, value: bool):
        self.__debug = value

        for handler in logging.getLogger().handlers:
            if self.__debug:
                handler.setLevel(logging.DEBUG)

    def __configure(self) -> None:
        with self.FILEPATH.open() as file:
            config = yaml.safe_load(file)
            logging.config.dictConfig(config)


manager = LogManager()
