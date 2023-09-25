import logging
import sys
from typing import Optional, Tuple

class LevelFormatter(logging.Formatter):
    """Provide differentiated log message formatting based on the logger's
    level"""

    _DEFAULT_FORMATTER = logging.Formatter(
        "%(asctime)s %(name)s [%(levelname)s] [%(module)s] %(message)s"
    )

    _DEBUG_FORMATTER = logging.Formatter(
        "%(asctime)s %(name)s (%(funcName)s @ %(filename)s:%(lineno)d) "
        "[%(levelname)s] %(message)s"
    )

    def __init__(self, *args, logger: logging.Logger, **kwargs):
        """Sets up the formatter to track a given logger

        Args:
            logger: A mandatory kw argument specifying the logger to which the
                    formatter will be attached to.
                    When formatting a message, the formmater will use the
                    appropriate message format given the logger's level at the
                    time

        """
        self._logger = logger
        self._formatters = {
            logging.INFO: self._DEFAULT_FORMATTER,
            logging.DEBUG: self._DEBUG_FORMATTER,
        }
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        try:
            return self._formatters[self._logger.level].format(record)
        except KeyError:
            return self._DEFAULT_FORMATTER.format(record)

def setup_logger(logger_name: Optional[str] = None) -> logging.Logger:
    # Get the root logger
    logger = logging.getLogger(logger_name)

    # Do not propagate to the root logger
    logger.propagate = False

    # Set default logging level
    logger.setLevel(logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stderr)

    # Set format for console handler
    console_handler.setFormatter(LevelFormatter(logger=logger))

    # Purge any previously registered handlers on the logger
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Register console handler
    logger.addHandler(console_handler)

    return logger

def set_logging_level(
        level: int,
        logger: logging.Logger,
        propagate: bool = False,
        upstream_loggers: Tuple[logging.Logger, ...] = (logging.getLogger(),)
    ):
    """Change the logging level for the logger(s)

    Args:
        level: The logging level. See the `logging` module for more info
        propagate: Whether to propage the logging level change to loggers of
                   upstream dependencies
    """
    logger.setLevel(level)
    # Upstream loggers
    if propagate:
        for logger in upstream_loggers:
            logger.setLevel(level)
    else:
        # Don't want to see flood from imported modules
        for logger in upstream_loggers:
            logger.setLevel(logging.WARN)