


class IMPORT_MYSQL_EXCEPTION:
    # 导入MySQL异常环境
    try:
        from pymysql import Error
        from pymysql import DataError
        from pymysql import DatabaseError
        from pymysql import InternalError
        from pymysql import InterfaceError
        from pymysql import OperationalError
        from pymysql import ProgrammingError
    except:
        pass


    class NoUser(Exception): ...
    class NoPasswd(Exception): ...
    class NoData(Exception): ...
    class NoSelectDatabase(Exception): ...
    class ExeceedLimit(Exception): ...


class Catch:
    def __init__(self):
        pass

    @staticmethod
    def Process():
        # 进程异常
        def wrapper(*args, **kwargs):
            pass
        return wrapper
    

    @staticmethod
    def Net():
        # 网络异常捕获
        def wrapper(*args, **kwargs):
            pass
        return wrapper
    

    @staticmethod
    def DataBase():
        # 数据库异常
        def wrapper(*args, **kwargs):
            pass
        return wrapper
    
