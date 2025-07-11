# 导入MySQL相关异常
try:
    from pymysql import Error
    from pymysql import MySQLError
    from pymysql import DataError as MySQLDataError
    from pymysql import DatabaseError
    from pymysql import InternalError
    from pymysql import InterfaceError
    from pymysql import OperationalError
    from pymysql import ProgrammingError
except ImportError:
    pass

# 导入Redis相关异常
try:
    from redis import RedisError
    from redis import DataError as RedisDataError
    from redis import WatchError
    from redis import PubSubError
    from redis import TimeoutError
    from redis import ReadOnlyError
    from redis import ResponseError
    from redis import ConnectionError
    from redis import BusyLoadingError
    from redis import AuthenticationError
    from redis import ChildDeadlockedError
    from redis import AuthenticationWrongNumberOfArgsError
except ImportError:
    pass

# 导入Psutil相关异常
try:
    from psutil import NoSuchProcess
    from psutil import AccessDenied
except ImportError:
    pass

# 导入套接字相关异常
from socket import error

# 导入多进程相关异常
from multiprocessing import TimeoutError
from multiprocessing import ProcessError
from multiprocessing import AuthenticationError

# 导入JSON相关异常
from json import JSONDecodeError

# 导入自定义默认异常
from .default import *