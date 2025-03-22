from socket import socket
from socket import error as SockError
from functools import wraps

from ._catch import __CatchBase, Logger
from ._catch import LOGSPATH, LIBPATH


class _CatchSock(__CatchBase):
    log_path = LOGSPATH.bind(LIBPATH)
    logger = Logger(
        name="sock", 
        log_file="socket.log",
        log_path=log_path
    )
    socks = []
    
    def sock(self, func):
        @wraps(func)
        def wrapper(sock:socket, *args, **kwargs):
            try:
                sock.getpeername()
                self.record(func)
            except SockError as e:
                self.record(func, e, 3)
                return False
            return func(*args, **kwargs)
        return wrapper
    
    def checksockconning(self, func):
        # 校验SOCK连接状态
        @wraps(func)
        def wrapper(sock:socket, *args, **kwargs):
            try:
                sock.getpeername()
                self.record(func)
            except SockError:
                self.record(func, "连接错误", 3)
                return "连接错误"
            return func(sock, *args, **kwargs)
        return wrapper