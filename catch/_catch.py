import inspect
from functools import wraps

from lib.manager._logger import Logger


class __CatchBase:
    logger = Logger("catch", log_file="sys.log")
    def __init__(self):
        self.logs = []
    
    # 默认捕获器
    def catch(self, *args, **kwargs):
        """
            额外的日志说明
        log attr:
            instruct: "sudo apt update"
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
    
    def timeout(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.record(func)
                return func(*args, **kwargs)
            except TimeoutError:
                self.record(func, "Timeout", 3)
                return False
        return wrapper
    
    def record(self, func, msg="success", level=1):
        logtext = self.logger.format_logtext(func.__name__, msg, module=func.__module__)
        self.logger.record(level, logtext)
    
    
    def __close__(self):
        for close in self.CLOSE:
            close.close()

    


    # def __log_record(self, func, msg="success", level=0):
    #     """
    #     0: debug
    #     1: info
    #     2: waring
    #     3: error
    #     4: critical
    #     """
    #     logtext = logger.format_logtext(func.__name__, msg, model = func.__module__, path = inspect(func))
    #     logger.record(level, logtext)