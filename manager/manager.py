import re
from pathlib import Path


from .__catch import Catch
from .__logger import Logger
from ..init.resolver import __resolver


DEFAULT = __resolver("default")
CONFLOGS = DEFAULT.search("log-settings")
level = CONFLOGS.search("level")


#  读取默认日志级别
if re.match(r"^(0|d|(debug))$", level.data.lower()):
    LEVEL = 0
elif re.match(r"^(2|w|(warning))$", level.data.lower()):
    LEVEL = 2
elif re.match(r"^(3|e|(error))$", level.data.lower()):
    LEVEL = 3
elif re.match(r"^(4|c|(critical))$", level.data.lower()):
    LEVEL = 4
else:
    # 始终默认使用Info级别日志
    LEVEL = 1


# logger = Logger(
#     level=LEVEL
# )

print(__file__)
class Managers:
    cwd = Path.cwd()
    def __init__(self):
        pass



__all__ = [
    "Logger",
    "Managers",
    "LEVEL"
]