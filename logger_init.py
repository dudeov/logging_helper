import logging
from logger_setup import setup_logger, set_logging_level
from functools import partial

########### if we place the file `logger_setup.py` right in the project ###########
## We can initialize logger object right in there at the end and skip this file ##
LOGGER_NAME = "My project name"
LOGGER: logging.Logger = setup_logger(LOGGER_NAME)
## and pass that LOGGER in the function `set_logging_level`
## Thus we could import and use `LOGGER` and `set_logging_level` directly from `logger_setup.py`

########### if`logger_setup.py` is a lib and imported from another repo ###########
## This we can know the LOGGER_NAME in advance and should re-init function in our repo
## passing the name of the LOGGER we just created
set_logging_level = partial(set_logging_level, logger=LOGGER)