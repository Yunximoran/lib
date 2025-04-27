import platform

from .windows import Windows
from .linux import Linux
from ._base import Information

def System():
    OS = platform.system()

    if OS == "Windows":
        return Windows()
    elif OS == "Linux":
        return Linux()
    else:
        raise "系统标识错误"