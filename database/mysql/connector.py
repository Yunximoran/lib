from pymysql import Connect
from pymysql.cursors import Cursor

from ..._init import _resolver
from ..._catch import _Catch, _Logger
from ..._catch import CatchMySQLEvent as catch_event
from ..._catch._execption import NoUser, NoPasswd

"""
WorkBench操作层
数据处理层
构造SQL语句
"""

class Connector:
    logger = _Logger("dbmq")
    catch = _Catch(logger)
    _conf = _resolver("database", "mysql")
    _host = _conf.search("host").data
    _port = _conf.search("port").data
    _usedb = _conf.search("db").data

    try: _user = _conf['user']
    except Exception: raise NoUser("never set mysql user")
    try: _passwd = _conf.password
    except Exception: raise NoPasswd("never set mysql passwd")

    def __init__(self, *, host:str = _host, port: int = _port, user: str = _user, passwd: str = _passwd, usedb:str = _usedb):
        self._conn: Connect = self._login_(host, port, user, passwd)
        if usedb:
            self._usedb = usedb
        self._conn.select_db(self._usedb)
        self._cursor = self._conn.cursor()
        self.logger.record(1, "connect to mysql service, current: {}".format(self._usedb))

    @catch.MySQL(catch_event.CONNECT)
    def _login_(self, host:str = None, port: int = None, user: str = None, passwd: str = None):
        return Connect(
            host=host,
            port=port,
            user=user,
            password=passwd,
            autocommit=True
        )
    @catch.MySQL(catch_event.EXECUTE)
    def execute(self, sql):
        self._cursor.execute(str(sql))
        return tuple([row if len(row) > 1 else row[0] for row in self._cursor.fetchall()])
    
    def getconn(self) -> Connect:
        return self._conn
    
    def getcurosr(self) -> Cursor:
        return self._cursor
    
    def using(self):                                            # 查看当前正在使用的数据库
        return self._usedb
    
    def results(self):
        results = self._cursor.fetchall()
        return tuple([row if len(row) > 1 else row[0] for row in results])

    def close(self):
        self._conn.close()
        self._cursor.close()