import re, logging, inspect
from functools import wraps

from ._execption import *
from .logs import _Logger

class CatchSystemEvent:
    PROCESS = 0

class CatchProcessEvent:
    pass

class CatchMySQLEvent:
    CONNECT = 0
    EXECUTE = 1
    SELECT = 2

class _Catch:
    # 进程序列
    def __init__(self, logger:_Logger):
        self.logger = logger

    def Process(self, func):
        # 进程异常
        @wraps(func)
        def wrapper(cls, target, *args, **kwargs):
            if "attribute" in kwargs: # 补充函数缺失属性
                attribute:dict = kwargs['attribute']
                for opt, val in attribute.items():
                    setattr(target, opt, val)
                del kwargs["attribute"]
            _name_ = target.__name__
            _module_ = inspect.getsourcefile(target)
            _deline_ = inspect.getsourcelines(target)[1]

            # hasattr()
            try:
                res = target(*args, **kwargs)
                self.logger.record(1, "Process Task: {}".format(_name_), "File \"{}\", line {}".format(_module_, _deline_))
                return res
            except KeyboardInterrupt:
                return False
            except ZeroDivisionError:
                self.logger.record(3, "Test Catch Process")
                return False
        return wrapper
    
    def NetWork(self):
        # 网络异常捕获
        def wrapper(*args, **kwargs):
            pass
        return wrapper
    
    def DataBase(self):
        # 数据库异常
        def wrapper(*args, **kwargs):
            pass
        return wrapper
    
    def MySQL(self, type):
        if type == CatchMySQLEvent.CONNECT:
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    try:
                        return func(*args, **kwargs)
                    except OperationalError as e:
                        self.logger.record(3, e)
                        return False
                return wrapper
            return decorator
        
        if type == CatchMySQLEvent.EXECUTE:      
            def decorator(func):
                @wraps(func)
                def wrapper(cls, SQL):
                    try:
                        res = func(cls, SQL)
                        self.logger.record(1, SQL)
                        return res
                    except MySQLDataError as e:
                        self.logger.record(3, "mysql error: {args}")
                        cls._conn.rollback()
                        return False
                    except ProgrammingError as e:
                        self.logger.record(3, e)
                        return False
                    except OperationalError as e:
                        self.logger.record(2, e)
                        return False
                return wrapper
            return decorator
    
    def MonGo(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                pass
            return wrapper
        return decorator
    
    def Redis(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    res = func(*args, **kwargs)
                    self.logger.record(1, *args, **kwargs)
                    return res
                except ConnectionError as e:
                    self.logger.record(3, e)
                    return False
            return wrapper
        return decorator
    
    def JSON(self, name, *, isclass=False, ignore=False):
        """
        :param name: JSON作用对象
        :param isclass: 区分方法/函数
        :param ignore: 只做捕获, 忽略日志输出

        :type name: str
        :type isclass: bool
        :type ignore: bool
        """
        if isclass:
            def decorator(func):
                @wraps(func)
                def wrapper(cls, *args, **kwargs):
                    try:
                        res = func(cls, *args, **kwargs)
                        if not ignore: self.logger.record(1, "finished {}".format(name))
                        return res
                    except JSONDecodeError:
                        if not ignore: self.logger.record(2, "finished {}".format(name))
                        return False
                    except TypeError:
                        if not ignore: self.logger.record(2, "finished {}".format(name))
                        return False
                return wrapper
            return decorator
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    res = func(*args, **kwargs)
                    if not ignore: self.logger.record(1, "finished {}".format(name))
                    return res
                except JSONDecodeError:
                    if not ignore: self.logger.record(3, "unfinished {}".format(name), *args, **kwargs)
                    return False
                except TypeError:
                    if not ignore: self.logger.record(2, "unfinished {}".format(name), *args, **kwargs)
                    return False
            return wrapper
        return decorator

    def System(self, type):
        if type == CatchSystemEvent.PROCESS:
            def decorator(func):
                @wraps(func)
                def wrapper(cls, path, process):
                    try:
                        checked_process = func(cls, path, process)
                        return checked_process
                    except NoSuchProcess:
                        self.logger.record(2, "NoSuchProcess {}".format(process.name()))
                        return False
                    except AccessDenied:
                        self.logger.record(3, "AccessDenied {}".format(process.name()))
                        return False
                return wrapper
            return decorator
        raise CatchSystemTypeError("System Excetpion Type Set Error")
    
__all__ = [
    "CatchSystemEvent",
    "CatchProcessEvent",
    "CatchMySQLEvent"
]