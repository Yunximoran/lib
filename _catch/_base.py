import re, logging, inspect
from typing import Callable
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
    CATCH_REDIS_CONNECT = True
    CATCH_REDIS_TIMEOUT = True
    CATCH_REDIS_DATA = True
    CATCH_REDIS_WATCH = True
    CATCH_REDIS_RESPONSE = True
    CATCH_REDIS_READONLY = True

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
    
    def DataBase(self, cache, disk, *,
                callback:Callable=None,
                error_callback:Callable=None
            ):
        """
        :param cache: 缓存数据库(Redis)
        :param disk: 磁盘数据库(MySQL)
        :param callback: 正常运行时触发事件函数
        :param callback: 异常时触发事件函数
        """
        # 复合数据库异常处理
        def decorator(func):
            @wraps(func)
            def wrapper(cls, *args, **kwargs):
                catched = True
                try:
                    res = func(cls, *args, **kwargs)
                    self.logger.record(1, *args)
                    catched =False
                    return res
                except ConnectionError:
                    self.logger.record(1, "捕获到一个Connect异常")
                    return False
                except TimeoutError:
                    self.logger.record(3, "捕获到一个Timemout异常")
                    return False
                except RedisDataError:
                    self.logger.record(3, "捕获到一个Redis写入异常")
                    return False
                except MySQLDataError:
                    self.logger.record(3, "捕获到一个MySQL写入异常")
                    return False
                finally:
                    if not catched:
                        if callback:\
                        callback(res);\
                        self.logger.record(1, "回调函数")
                    else:
                        if error_callback:\
                        error_callback(cls, *args, **kwargs);\
                        self.logger.record(2, "捕获到缓存异常，做降级处理， 数据写入MySQL")
            return wrapper
        return decorator

    
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
    
    def Redis(self, *, 
            connect=CATCH_REDIS_CONNECT,
            timeout=CATCH_REDIS_TIMEOUT,
            data=CATCH_REDIS_DATA,
            watch=CATCH_REDIS_WATCH,
            response=CATCH_REDIS_RESPONSE,
            readonly=CATCH_REDIS_READONLY,
        ):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    res = func(*args, **kwargs)
                    self.logger.record(1, *args, **kwargs)
                    return res
                except ConnectionError as e: # Redis连接异常，Redis服务器连接失败时触发
                    self.logger.record(3, "Redis 连接错误， Redis服务是否运行 或者 Redis配置是否正确")
                    if connect: return False
                    raise e
                except TimeoutError as e:    # 超时异常， Redis命令超时时触发
                    self.logger.record(2, "Redis 超时", "未运行", *args[1:])
                    if timeout: return False
                    raise e
                except WatchError as e:
                    if watch: return False
                    raise e
                except RedisDataError as e:
                    if data: return False
                    raise e
                except ResponseError as e:
                    if response: return False
                    raise e
                except ReadOnlyError as e:
                    if readonly: return False
                    raise e
                finally:
                    pass
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