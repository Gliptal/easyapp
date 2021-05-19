from __future__ import annotations

import logging
import pathlib
import typing

import confuse
from ruamel import yaml

import easyapp.utils.path as path


logger = logging.getLogger(__name__)


class ConfigFile:

    def __init__(self, path: pathlib.Path):
        self.path = path

        self.lazy = False

    def __getitem__(self, key: str) -> typing.Any:
        get_view = key[0] == "/"

        if get_view:
            key = key[1:]

        parts = key.split("/")

        value = self.__view[parts[0]]
        for part in parts[1:]:
            value = value[part]

        return value if get_view else value.get()

    def __setitem__(self, key: str, item: typing.Any):
        self[f"/{key}"].set(item)

        if not self.lazy:
            self.save()

    @property
    def path(self) -> pathlib.Path:
        return self.__path

    @path.setter
    def path(self, value: pathlib.Path):
        self.__path = pathlib.Path(value)

        self.__view = confuse.LazyConfig("")
        self.load()

    def load(self) -> None:
        logger.debug(f"loading from configuration file \"{path.shorten_path(self.path)}\"")

        self.__view.set_file(self.path)

    def save(self) -> None:
        logger.debug(f"saving to configuration file \"{path.shorten_path(self.path)}\"")

        with self.path.open("w") as file:
            parser = yaml.YAML(typ="safe")
            data = parser.load(self.__view.dump())

            parser = yaml.YAML()
            parser.default_flow_style = False
            parser.indent(mapping=4, sequence=6, offset=4)

            parser.dump(data, file)

    def reload(self) -> None:
        self.save()
        self.load()


class ConfigManager:

    def __init__(self) -> None:
        #yapf: disable
        self.info      = ConfigFile(path.cwd_path("config/easyapp/info.yml"))
        self.arguments = ConfigFile(path.cwd_path("config/easyapp/arguments.yml"))
        self.configs   = self.__find_configs()
        #yapf: enable

        self.lazy = False

    def __getitem__(self, key: str):
        return self.configs[key]

    @property
    def configs(self) -> dict[str, ConfigFile]:
        return self.__configs

    @configs.setter
    def configs(self, value: dict[str, ConfigFile]):
        self.__configs = value

    @property
    def lazy(self) -> bool:
        return self.__lazy

    @lazy.setter
    def lazy(self, value: bool):
        self.__lazy = value

        for config in self.configs.values():
            config.lazy = self.__lazy

    def __find_configs(self) -> dict[str, ConfigFile]:
        dir = pathlib.Path("config")
        files = sorted(dir.glob("*.yml"))

        logger.debug(f"found {len(files)} user config file(s)")

        configs = {}
        for config in files:
            configs[config.stem] = ConfigFile(path.cwd_path(config))

        return configs
