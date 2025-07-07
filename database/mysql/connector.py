from pymysql import Connect
from pymysql.cursors import Cursor

from .dispose._exception import NoUser, NoPasswd
from ...init.resolver import __resolver

"""
WorkBench操作层
数据处理层
构造SQL语句
"""

CONF = __resolver("mysql")
HOST = CONF.search("host").data
PORT = CONF.search("port").data
USEDB = CONF.search("db").data

# MySQL user 和 passwd是必须的
try: USER = CONF['user']
except Exception: raise NoUser("error user")

try:PASSWORD = CONF.password
except Exception: raise NoPasswd("error passwd")

class Connector:
    def __init__(self, usedb:str = None):
        self.__conn = Connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            autocommit=True
        )
        if usedb:
            self.__usedb = usedb
        else:
            self.__usedb = USEDB
        self.__conn.select_db(self.__usedb)
        self.__cursor = self.__conn.cursor()

    
    def execute(self, sql):
        try:
            self.__cursor.execute(str(sql))
        except Exception as e:
            print(f"Error: SQL:\n\t{sql}\n") 
            self.__conn.rollback()
            return False
        return tuple([row if len(row) > 1 else row[0] for row in self.__cursor.fetchall()])
    
    def getconn(self) -> Connect:
        return self.__conn
    
    def getcurosr(self) -> Cursor:
        return self.__cursor
    
    def using(self):                                            # 查看当前正在使用的数据库
        return self.__usedb
    
    def results(self):
        results = self.__cursor.fetchall()
        return tuple([row if len(row) > 1 else row[0] for row in results])

    def close(self):
        self.__conn.close()
        self.__cursor.close()