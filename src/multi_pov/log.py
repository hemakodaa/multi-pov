import logging
from constants import LOGGER_BASE


def make_log(name: str = LOGGER_BASE) -> logging.Logger:
    base_logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh = logging.FileHandler(filename="multipov.log")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    base_logger.setLevel(logging.DEBUG)
    base_logger.addHandler(ch)
    base_logger.addHandler(fh)
    return base_logger


def log_main(name: str = LOGGER_BASE):
    logger = logging.getLogger(name)
    return logger
