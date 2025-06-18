from typing import Iterable


class Check:
    @staticmethod
    def checkLen(items: Iterable) -> bool:
        # 字典中可以获取到行数，数组中可以获取到列数
        # 检查预处理

        iNum = None
        for item in items:
            # 如果item不是可迭代对象，单条插入
            if not isinstance(item, Iterable) and iNum is None:
                return items
            lens = len(item)

            # 记录第一行[列]长度
            if iNum is None: iNum = lens; continue

            # 如果有一行[列]长度不一致返回False
            if iNum != lens: return False
            else: iNum = lens
        return True

    @staticmethod
    def checkInsertOnce(items):
        # 检查是否是单条数据插入
        # [t1, t2, t3] | [[],[],[]]
        # 这里只能校验格式化后的数据格式化后的数据
        for item in items:
            # 变量容器
            if isinstance(item, (list, tuple)):
                return False
        return True

    def checkUniformity(self, vals):
        # 校验数据是否一致
        # 单条数据不需要检查
        checkDataType = []
        if self.checkInsertOnce(vals):
            return True
        for items in vals:
            if not checkDataType:
                for item in items:
                    checkDataType.append(type(item))
                continue
            for i in range(len(checkDataType)):
                if not isinstance(items[i], checkDataType[i]):
                    return False
        return True

    # def checkKeyValNumEquality(self, db, tb, itemNum):
    #     # 检验键值是否对应
    #     # 也是只能校验格式化后的数据
    #     _, keyNum = self.info.get_fetchs(db, tb)
    #     print(keyNum)
    #     return True if keyNum == itemNum else False


