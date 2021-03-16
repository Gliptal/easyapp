import enum
import logging
import pathlib

import confuse

import easyapp.utils.path as path


logger = logging.getLogger(__name__)


class ConfigFiles(enum.Enum):
    #yapf: disable
    INFO      = enum.auto()
    ARGUMENTS = enum.auto()
    CONFIGS   = enum.auto()
    #yapf: enable


class ConfigManager:

    #yapf: disable
    FILEPATHS = {
        ConfigFiles.INFO      : path.cwd_path("config/easyapp/info.yml"),
        ConfigFiles.ARGUMENTS : path.cwd_path("config/easyapp/arguments.yml"),
        ConfigFiles.CONFIGS   : {}
    }
    #yapf: enable

    def __init__(self) -> None:
        #yapf: disable
        self.info      = None
        self.arguments = None
        self.configs   = {}
        #yapf: enable

        self.__find_configs()
        self.__load_configs()

    def __find_configs(self) -> None:
        dir = pathlib.Path("config")
        configs = sorted(dir.glob("*.yml"))

        logger.debug(f"found {len(configs)} config file(s)")

        for config in configs:
            self.FILEPATHS[ConfigFiles.CONFIGS][config.stem] = path.cwd_path(config)

    def __load_configs(self) -> None:
        self.info = confuse.LazyConfig("")
        self.arguments = confuse.LazyConfig("")

        self.info.set_file(self.FILEPATHS[ConfigFiles.INFO])
        self.arguments.set_file(self.FILEPATHS[ConfigFiles.ARGUMENTS])

        for config in self.FILEPATHS[ConfigFiles.CONFIGS]:
            self.configs[config] = confuse.LazyConfig("")
            self.configs[config].set_file(self.FILEPATHS[ConfigFiles.CONFIGS][config])


manager = ConfigManager()
