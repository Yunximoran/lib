from socket import socket
from socket import error as SockError
from functools import wraps

from ._catch import __CatchBase, Logger


class _CatchSock(__CatchBase):
    logger = Logger("sock", log_file="socket.log")
    socks = []
    def __init__(self):
        pass
    
    def sock(self, func):
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
        def wrapper(sock:socket, *args, **kwargs):
            try:
                sock.getpeername()
                self.record(func)
            except SockError:
                self.record(func, "连接错误", 3)
                return "连接错误"
            return func(sock, *args, **kwargs)
        return wrapper