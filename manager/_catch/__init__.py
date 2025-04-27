from pathlib import Path
from functools import wraps

from .._logger import Logger

class catch:
    def __init__(self, logger:Logger):
        self.logger = logger

    # 默认捕获器
    def catch(self, *args, **kwargs):
        """
            额外的日志说明
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    self.record(func, 0)
                    return func(*args, **kwargs)
                except Exception:
                    return False
                except KeyboardInterrupt:
                    self.record(func, "The Ctrl C Single is teriggered", 3)
                    return False
                finally:
                    return None
            return wrapper
        return decorator
    
    # @staticmethod
    def timeout(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.record(func)
                _ = func(*args, **kwargs)
                return _
            except TimeoutError:
                self.record(func, "Timeout", 3)
                return False
        return wrapper
    
    def record(self, func, msg="success", level=1, *, logger:Logger=None):
        if logger is None:
            logger = self.logger
        logtext = logger.format_logtext(func.__name__, msg, module=func.__module__)
        logger.record(level, logtext)


    
