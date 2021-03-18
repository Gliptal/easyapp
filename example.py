import logging

# import the easyapp module to start the app
import easyapp

# define a logger
logger = logging.getLogger(__name__)

# access commandline arguments in the ARGS module variable
args = easyapp.ARGS

# access config files in the CONFIGS module variable
configs = easyapp.CONFIGS

# get a config file indexing its name
config = configs["config"]

# get a config value by indexing its hierarchical path
value = config["path/to/value"]

# get a confuse view by indexing its hierarchical path prepended by a '/'
view = config["/path/to/value"]

# set a config value by assignment
config["path/to/value"] = value

# save the current configuration to the config file
config.save()
