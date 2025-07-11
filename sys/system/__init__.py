import platform
from ._base import _BaseSystem
from .windows import Windows
from .linux import Linux

def System():
    OS = platform.system()
    if OS == "Windows":
        return Windows()
    elif OS == "Linux":
        return Linux()
    else:
        raise "系统标识错误"