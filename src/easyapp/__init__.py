import easyapp.utils
import easyapp.log
import easyapp.config
import easyapp.arguments


ARGS = None
CONFIGS = {}


def __init():
    global ARGS
    ARGS = easyapp.arguments.parser.args

    global CONFIGS
    CONFIGS = easyapp.config.manager.configs

    easyapp.log.manager.debug = ARGS.debug


def __log_status():
    import importlib.metadata
    import logging

    #yapf: disable
    app_name        = easyapp.config.manager.info['name'].get()
    app_version     = easyapp.config.manager.info['version'].get()
    easyapp_version = importlib.metadata.version('easyapp-gliptal')
    #yapf: enable

    logger = logging.getLogger(__name__)
    logger.info(f"starting {app_name} v{app_version} (powered by easyapp v{easyapp_version})")


__init()
__log_status()
