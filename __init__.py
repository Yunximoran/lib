from pathlib import Path
from ._init import *
from ._catch import _Catch, _Logger

class Logger(_Logger):
    _conf = resolver("log-settings")
    log_path = Path(__file__).parent / Path("../logs")
    log_path = log_path.resolve()
    log_path.mkdir(parents=True, exist_ok=True)


class Catch(_Catch):
    pass


# 导出常用处理工具
if __name__ == "__main__":
    pass