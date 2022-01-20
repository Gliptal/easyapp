import argparse
import logging

import confuse.exceptions

import easyapp.config


logger = logging.getLogger(__name__)


class CommandlineParser:

    def __init__(self, config: easyapp.config.ConfigManager):
        self.__config = config

        self.__parser = argparse.ArgumentParser()

        self.__add_info()
        self.__add_required()
        self.__add_switches()
        self.__add_flags()

    @property
    def args(self) -> argparse.Namespace:
        logger.debug("parsing command-line options")

        args = self.__parser.parse_args()

        logger.debug(f"parsed options {args}")

        try:
            for required in self.__config.arguments["required"]:
                try:
                    option = getattr(args, required['name'])
                    if option not in required["values"]:
                        raise argparse.ArgumentTypeError(f"\"{option}\" is not an accepted option for required argument \"{required['name']}\"")
                except KeyError:
                    pass
        except confuse.exceptions.NotFoundError:
            pass

        return args

    def __add_info(self):
        self.__parser.description = self.__config.info["pitch"]
        self.__parser.epilog = self.__config.info["description"]

        self.__parser.add_argument("-v", "--version", action="version", version=self.__config.info["version"])

    def __add_required(self):
        group = self.__parser.add_argument_group()

        try:
            for argument in self.__config.arguments["required"]:
                type = globals()["__builtins__"][argument["type"]]
                group.add_argument(argument["name"], type=type, help=argument["help"])
        except confuse.exceptions.NotFoundError:
            pass

    def __add_switches(self):
        group = self.__parser.add_argument_group()

        try:
            for argument in self.__config.arguments["switches"]:
                group.add_argument(f"-{argument['handle']}", f"--{argument['name']}", action="store_true", help=argument["help"])
        except confuse.exceptions.NotFoundError:
            pass

    def __add_flags(self):
        group = self.__parser.add_argument_group()

        try:
            for argument in self.__config.arguments["flags"]:
                type = globals()["__builtins__"][argument["type"]]
                group.add_argument(f"-{argument['handle']}", f"--{argument['name']}", type=type, default=argument["default"], help=argument["help"])
        except confuse.exceptions.NotFoundError:
            pass
