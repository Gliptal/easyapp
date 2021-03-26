import argparse
import logging

import confuse.exceptions

from easyapp.config import manager as config


logger = logging.getLogger(__name__)


class CommandlineParser:

    def __init__(self):
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

        for required in config.arguments["required"]:
            option = getattr(args, required['name'])
            if option not in required["values"]:
                raise argparse.ArgumentTypeError(f"\"{option}\" is not an accepted option for required argument \"{required['name']}\"")

        return args

    def __add_info(self) -> None:
        self.__parser.description = config.info["pitch"]
        self.__parser.epilog = config.info["description"]

        self.__parser.add_argument("-v", "--version", action="version", version=config.info["version"])

    def __add_required(self) -> None:
        group = self.__parser.add_argument_group()

        try:
            for argument in config.arguments["required"]:
                group.add_argument(argument["name"], help=argument["help"])
        except confuse.exceptions.NotFoundError:
            pass

    def __add_switches(self) -> None:
        group = self.__parser.add_argument_group()

        try:
            for argument in config.arguments["switches"]:
                group.add_argument(f"-{argument['handle']}", f"--{argument['name']}", action="store_true", help=argument["help"])
        except confuse.exceptions.NotFoundError:
            pass

    def __add_flags(self) -> None:
        group = self.__parser.add_argument_group()

        try:
            for argument in config.arguments["flags"]:
                type = globals()["__builtins__"][argument["type"]]
                group.add_argument(f"-{argument['handle']}", f"--{argument['name']}", type=type, default=argument["default"], help=argument["help"])
        except confuse.exceptions.NotFoundError:
            pass


parser = CommandlineParser()
