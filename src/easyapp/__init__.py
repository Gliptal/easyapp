import easyapp.utils
import easyapp.log
import easyapp.arguments
import easyapp.config


ARGS = None
CONFIGS = None


def __init():
    import importlib.metadata
    import logging

    config = easyapp.config.ConfigManager()
    arguments = easyapp.arguments.CommandlineParser(config)

    global ARGS
    global CONFIGS
    ARGS = arguments.args
    CONFIGS = config.configs

    easyapp.log.debug(ARGS.debug)

    #yapf: disable
    app_name        = config.info["name"]
    app_version     = config.info["version"]
    try:
        easyapp_version = importlib.metadata.version("easyapp")
    except importlib.metadata.PackageNotFoundError:
        easyapp_version = "0.1.0"
    #yapf: enable

    logger = logging.getLogger(__name__)
    logger.info(f"starting {app_name} v{app_version} (powered by easyapp v{easyapp_version})")


__init()
