from functools import wraps
# from redis import ConnectionError

from ._catch import __CatchBase, Logger

class _CatchDataBase(__CatchBase):
    logger = Logger("database", log_file="database.log")
    def __init__(self):
        pass
    
    def ping(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ConnectionError:
                return "无连接"
        return wrapper
        
    def redis(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.record(func)
                return func(*args, **kwargs)
            except ConnectionError:
                self.record(func, "无法连接Redis", 3)
                return "无法连接redis"
        return wrapper
    
    def mysql(self, func):
        @wraps
        def wrapper(*args, **kwargs):
            try:
                self.record(func)
                return func(*args, **kwargs)
            except ConnectionAbortedError:
                self.record("func", "无法连接MySQL", 3)
                return "无法连接MySQL"
        return wrapper