from .check import Check
from .construction import Rows


class Formation:
    """
    数据格式化
    formatDict:     格式化字典数据
    formatSeries:   格式化矩阵数据
    """
    def __init__(self):
        self.check = Check()

    def formatDict(self, data:dict):
        # 从字典中提取列名和列数据
        keys = tuple(data.keys())
        vals = tuple(data.values())
        # 校验数据长度是否一致，获取更新次数
        check = self.check.checkLen(vals) 

        # 如果只有一条数据，vals是一维数组，无法被二次遍历
        if check:
            if check == vals:
                return Rows(vals), keys
            # 格式化成行数据
            vals = tuple(self.__formatDict(vals))
        else:
            return None, None
        return Rows(*vals), keys
    
    @staticmethod
    def __formatDict(items):
        iters = len(items[0])  # 获取行数
        for i in range(iters):
            yield tuple([item[i] for item in items])

    def formatSeries(self, data):
        # [[],[],[],[],[],[]]
        vals = tuple(data)
        check = self.check.checkLen(vals)
        if check:
            if check == vals:
                return Rows(vals), () # len(vals)
            # 格式化成行数据
            vals = tuple(self.__formatSeries(vals))
        else:
            return None, None
        return Rows(*vals), ()

    @staticmethod
    def __formatSeries(data):
        for val in data:
            yield tuple(val)
