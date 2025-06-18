from pathlib import Path

from ._logger import Logger
from ._catch import catch


class Managers:
    cwd = Path.cwd()
    def __init__(self):
        pass

    def  getlogger(name, log_file, level):
        return Logger(name, log_file, level)

__all__ = [
    "Logger",
    "catch",
    "Managers"
]