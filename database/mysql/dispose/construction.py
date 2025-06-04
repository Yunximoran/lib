from typing import Iterable

from .constant import Fetch, Rows, Row
from ._exception import ExeceedLimit

class Construction:
    def __init__(self):
        self.basic = None

    def __str__(self):
        return self.basic
    

class Condition(Construction):
    def __init__(self, left=None, right=None, link="and"):
        self.commit = None
        self.basic = f"Where {self.commit}"
        if left or right:
            if link == "and":
                self.And(left, right)
            elif link == "or":
                self.Or(left, right)
        

    def And(self, left, right=None):
        if isinstance(left, Condition):
            left = left.commit if not left.commit else f"({left.commit})"
            
        if isinstance(right, Condition):
            right = right.commit if not right.commit else f"({right.commit})"
        elif right is None:
            right = self.commit if not self.commit else f"{self.commit}"

        if left and right:
            self.commit = f"{left} and {right}"
        else:
            if left:
                self.commit = left
            elif right:
                self.commit = right
            else:
                raise ValueError("left and right must exist")
            
        self.basic = f"Where {self.commit}"
        return f"{left} and {right}"

    def Or(self, left, right=None):        
        if isinstance(left, Condition):
            left = left.commit if left.commit is None else f"({left.commit})"
            
        if isinstance(right, Condition):
            if right.commit is None:
                right = right.commit
            else:
                right = f"({right.commit})"
        elif right is None:
            right = f"{self.commit}"

        if left and right:
            self.commit = f"{left} or {right}"
        else:
            if left:
                self.commit = left
            elif right:
                self.commit = right
            else:
                raise ValueError("left and right must exist")
            
        self.basic = f"Where {self.commit}"
        return f"{left} or {right}"

    def __str__(self):
        return f"{self.basic} "


class Create(Construction):
    def __init__(self, tbn:str, fetchs:tuple[Fetch], exists=True):
        """
        :param tbn: 表名
        :param fetchs: 表字段序列
        """
        fetchs = [str(fetch) for fetch in fetchs]
        if exists:
            self.basic = "Create Table if not exists {} ({})".format(tbn, ", ".join(fetchs))
        else:
            self.basic = "Create Table {} ({})".format(tbn, ", ".join(fetchs))


class Select(Construction):
    def __init__(self, tbn, find:Iterable[Fetch]=None, condition:Condition=None):
        self.table = tbn

        if find:
            self.select = []
            for fetch in find:
                if isinstance(fetch, Fetch): self.select.append(fetch.name)
                else: self.select.append(fetch)
            self.select = ", ".join(self.select)
        else:
            self.select = "*"

        if condition:
            if not isinstance(condition, Condition): raise TypeError("The condition must a Condition")
            self.basic = "Select {} From {} {}".format(self.select, self.table, condition)
            self.condition = condition
        else:
            self.basic = "Select {} From {}".format(self.select, self.table)
            self.condition = Condition()
    
    def And(self, left, right=None):
        self.condition.And(left, right)
        self.basic = "Select {} From {} {}".format(self.select, self.table, self.condition)
        return self.condition

    def Or(self, left, right=None):
        self.condition.Or(left, right)
        self.basic = "Select {} From {} {}".format(self.select, self.table, self.condition)
        return self.condition


class Insert(Construction):
    def __init__(self, tbn, vals:Rows|Row, keys=(), *, ignore=True):
        if len(keys) and len(keys) != vals.length:
            # 指定列时，每行的数量必须和指定列的数量一致
            raise ExeceedLimit("keys length must be equal to row length")
        
        if not isinstance(vals, Rows|Row):
            # 必须使用 Rows|Row 对数据进行包装
            raise TypeError("vals must type of Rows or Row")
        
        # 构造键值SQL命令
        commit_vals = self.commit_vals(vals)
        commit_keys = self.commit_keys(keys)

        # 设置忽略主键重复
        if not ignore:ignore = " "
        else:  ignore = " Ignore "

        # 构造完整Insert命令
        self.basic = "Insert{}Into {}{}Values {}".format(ignore, tbn, commit_keys, commit_vals)    
    
    def commit_vals(self, vals:Rows|Row):
        # 多行插入和单行插入
        if isinstance(vals, Row):
            return "({})".format(", ".join(vals))
        commit = ["({})".format(", ".join(val)) for val in vals]
        return ", ".join(commit)

    def commit_keys(self, keys:list[str|Fetch]):
        # 指定列和不指定列
        commit =  []
        for key in keys:
            if isinstance(key, Fetch):
                commit.append(key.name)
            elif isinstance(key, str): 
                commit.append(key)
            else: raise TypeError("key must type of Str or Fetch")

        if not commit: return " "
        else: return " ({}) ".format(", ".join(commit))


class Update(Construction):
    def __init__(self, tbn, condition:Condition=None, **datas):
        if not datas:
            raise ValueError("No Update Datas")
        self.table = tbn
        self.commit = []
        for fetch, data in datas.items():
            if not isinstance(data, str):
                print(fetch, data)
                data = str(data)
            # else:
            #     data = data
            self.commit.append("{} = {}".format(fetch, data))

        if condition:
            if not isinstance(condition, Condition): raise TypeError("The condition must a Condition")
            self.basic = "Update {} Set {} {}".format(self.table, ", ".join(self.commit), condition)
            self.condition = condition
        else:
            self.basic = "Update {} Set {}".format(self.table, ", ".join(self.commit))
            self.condition = Condition()

    def And(self, left, right=None):
        self.condition.And(left, right)
        self.basic = "Update {} Set {} {}".format(self.table, ", ".join(self.commit), self.condition)
        return self.condition

    def Or(self, left, right=None):
        self.condition.Or(left, right)
        self.basic = "Update {} Set {} {}".format(self.table, ", ".join(self.commit), self.condition)
        return self.condition


class Delete(Construction):
    def __init__(self, tbn, condition:Condition=None):
        self.table = tbn
        if condition:
            if not isinstance(condition, Condition): raise TypeError("The condition must a Condition")
            self.basic = "Delete From {} {}".format(self.table, condition)
            self.condition = condition
        else:
            self.basic = "Delete From {}".format(self.table)
            self.condition = Condition()

    def And(self, left, right=None):
        self.condition.And(left, right)
        self.basic = "Delete From {} {}".format(self.table, self.condition)
        return self.condition

    def Or(self, left, right=None):
        self.condition.Or(left, right)
        self.basic = "Delete From {} {}".format(self.table, self.condition)
        return self.condition

__all__ = [
    "Create",
    "Select",
    "Insert",
    "Update",
    "Delete",
    "Condition"
]
