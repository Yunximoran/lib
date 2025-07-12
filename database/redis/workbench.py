import os
import json
import re
from typing import List
from redis import StrictRedis

from lib._init import _resolver
from ..._catch import _Catch, _Logger


class Workbench(StrictRedis):
    """
        Redis操作模块, 只在redis服务启动后可用
    """
    logger = _Logger("dbr")
    catch = _Catch(logger)

    _conf = _resolver("database", "redis")
    _host = _conf.search("host").data
    _port = _conf.search("port").data
    _usedb = _conf.search("db").data

    try: _passwd = _conf.password
    except Exception: _passwd = None

    def __init__(self, *,
                connect=True, 
                timeout=True, 
                data=True, 
                watch=True, 
                response=True, 
                readonly=True,        
                ):
        super().__init__(
            host=self._host,
            port=self._port, 
            password=self._passwd, 
            db=self._usedb, 
            decode_responses=True)
        
        self.catch.CATCH_REDIS_CONNECT = connect
        self.catch.CATCH_REDIS_TIMEOUT = timeout
        self.catch.CATCH_REDIS_DATA = data
        self.catch.CATCH_REDIS_WATCH = watch
        self.catch.CATCH_REDIS_RESPONSE = response
        self.catch.CATCH_REDIS_READONLY = readonly

    def lrange(self, key, start = 0, end=None) -> list:
        if end is None:
            end = self.llen(key)
        return super().lrange(key, start, end)

    def save(self, **kwargs):
        return super().save(**kwargs)
        
    @catch.Redis()
    def execute_command(self, *args, **options):
        return super().execute_command(*args, **options)
    
    def loads(self, data, *, log_ignore=False):
        """
            读取redis数据, 转化为PYTHON对象
        """
        if not log_ignore: self.logger.record(1, f"Parse Redis Data: {data}")
        if isinstance(data, dict):
            results = {}
            for next in data:
                next_data = self.loads(data[next], log_ignore=True)
                results[next] = next_data
            return results
        
        if isinstance(data, list):
            results = []
            for next in data:
                next_data = self.loads(next, log_ignore=True)
                results.append(next_data)
            return results
        
        json_data = self.__loads(data)
        return self.loads(json_data, log_ignore=True) if json_data else data

    @catch.JSON("Parse Reids Data", isclass=True, ignore=True)
    def __loads(self, data):
        data = json.loads(data)
        return data

    

Redis = Workbench() 

if __name__ == "__main__":
    da = Redis.hgetall("classify")  
    a = Redis.loads(da)
    print(a)