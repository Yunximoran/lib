import os
import json
from redis import StrictRedis

from lib.init.resolver import __resolver
from lib.catch import _CatchDataBase

catch = _CatchDataBase()


HOST = __resolver("redis", "host")
PORT = __resolver("redis", "port")
DB = __resolver("redis", "db")
try:
    PASSWORD = __resolver("redis")["password"]
except Exception:
    PASSWORD = None
    
    
class Connector(StrictRedis):
    """
        Redis操作模块，只在redis服务启动后可用
    """
    def __init__(self, *args, **kwargs):
        super().__init__(
            host=HOST,
            port=PORT, 
            password=PASSWORD, 
            db=DB, 
            decode_responses=True)
        
    @catch.ping
    def status(self):
        self.ping()
    
    
    def lrange(self, key, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = self.llen(key)
        return super().lrange(key, 0, end)

    def save(self, **kwargs):
        return super().save(**kwargs)
        
    @catch.redis
    def execute_command(self, *args, **options):
        return super().execute_command(*args, **options)
    
    
    @catch.redis
    def dump(self, tbn, ft):
        with open(f"data/{tbn}.json", 'w', encoding="uft-8") as f:
            if ft == "dict":
                datas = self.hgetall(tbn)
            
            if ft == "list":
                datas = self.lrange(tbn)
            json.dump(datas, f)
    
    @catch.redis
    def load(self):
        workdir = os.getcwd()
        for child in os.listdir(os.path.join(workdir, "data")):
            if os.path.isfile(child):
                # 获取表名
                tbn = child.split(".")[0]
                with open(child, "r") as f:
                    datas = json.load(f)
                    if isinstance(datas, dict):
                        for k in datas:
                            self.hset(tbn, k, datas[k])
                    
                    if isinstance(datas, list):
                        for d in datas:
                            self.lpush(tbn, d)
                            

            
            
Redis = Connector()