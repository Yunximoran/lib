from ._tcp import _ProtoType


class Listener(_ProtoType):
    def listen(self): # 启用TCP监听
        pass
    
    def _task(self):  # 注册监听任务
        pass
    
    def parse(self):  # 解析TCP数据包
        pass
    