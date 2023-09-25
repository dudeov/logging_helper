from logger_init import LOGGER, set_logging_level
import logging

def get_logging_level_id_by_name(logging_level: str) -> int:
    return logging.getLevelName(logging_level.upper())

def main():
    LOGGER.info(f"Running the main func")
    set_logging_level(get_logging_level_id_by_name("warning"))
    LOGGER.info(f"This message is no longer printed")
    LOGGER.warning(f"Logging level has been changed")

main()

