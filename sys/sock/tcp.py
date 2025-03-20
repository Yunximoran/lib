import socket


class _ProtoType:
    def __init__(self, address, listens):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(address)
        self.sock.listen(listens)
    
    def settings(self):
        pass