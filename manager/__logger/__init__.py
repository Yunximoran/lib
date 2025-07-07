import re, logging

from logging.handlers import (
    RotatingFileHandler,
    TimedRotatingFileHandler
)


class Logger:
    __LEVELS = [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL
    ]
    def __init__(
            self, 
            level,
            encoding,
        ):
        self.level = self.__LEVELS[level]
        self.encoding = encoding
