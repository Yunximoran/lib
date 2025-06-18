from typing import Iterable

from .._exception import ExeceedLimit

class Meta(type):
    def __str__(cls):
        return cls.typeof
    
class Typeof(metaclass=Meta):
    def __init__(self, M, limit):
        if M not in limit:
            raise ExeceedLimit(":param M:{} limit: (0, 255)".format(M))
        self.typeof = f"{self.__class__.typeof}({M})"
    
    def __str__(self):
        return self.typeof


class Row:
    def __init__(self, *vals):
        self.vals = []
        self.mvals = []
        self.typeof = []
        self.length = 0
        for val in vals:
            self.push(val)

    def push(self, val):
        self.vals.append(val)
        self.typeof.append(type(val))
        self.length += 1
        if isinstance(val, str):
            self.mvals.append(f"'{val}'")
        else:
            self.mvals.append(str(val))

    def pop(self, index=-1):
        self.mvals.pop(index)
        self.length -= 1
        return self.vals.pop(index)
    
    def __len__(self):
        return self.length
    
    def __iter__(self):
        for val in self.mvals:
            yield val
    
    def __getitem(self, index):
        return self.vals[index]

class Rows:
    def __init__(self, *vals, **limit):
        self.vals: list[Row] = []
        self.length = None
        self.typeof = None

        if "length" in limit:
            self.length = limit['length']
            if not isinstance(self.length, int):
                raise TypeError("length must Int")
            
        if "typeof" in limit:
            self.typeof = limit['typeof']
            if not isinstance(self.typeof, Iterable):
                pass
            
        for val in vals:
            self.push(val)

    def push(self, val:Iterable):
        if isinstance(val, Iterable):
            if not isinstance(val, Row):
                val = Row(*tuple(val))
            self.vals.append(val)
            if self.length and self.length != len(val):
                # 检查数据长度
                raise ExeceedLimit("lengths of the subsequences must be consistent")
            else: self.length = len(val)
            if self.typeof and self.typeof != val.typeof:
                # 检查数据类型
                raise TypeError("typeof of the subsequences must be consistent")
            else: self.typeof = val.typeof
        else: raise TypeError("DataFrame Element Must Iterable")
    
    def pop(self, index=-1):
        self.vals.pop(index)

    def __len__(self):
        return len(self.vals)

    def __iter__(self):
        for val in self.vals:
            yield val

    def __getitem__(self, index:int):
        return self.vals[index]

class Fetch:
    def __init__(self, N:str, T:Typeof, *A):
        """
            ### 定义字段， 字段名, 字段类型, 字段属性|约束

        :param N: 字段名
        :param T: 字段类型
        :param A: 字段属性

        """
        self.name = N
        self.typeof = T
        self.attrib = A
        self.fetch = " ".join((N, str(T), *A))

    def __lt__(self, val):
        # 小于
        return f"{self.name} < {val}"
    
    def __gt__(self, val):
        # 大于
        return f"{self.name} > {val}"
    
    def __le__(self, val):
        # 小于等于
        return f"{self.name} <= {val}"
    
    def __ge__(self, val):
        # 大于等于
        return f"{self.name} >= {val}"
    
    def __eq__(self, val):
        # 等于
        return f"{self.name} = {val}"
    
    def __ne__(self, val):
        # 不等于
        return f"{self.name} != {val}"
    
    def In(self, right:Iterable):
        if not isinstance(right, Iterable):
            raise TypeError("In`s right must Iterable")
        return f"{self.name} in ({", ".join([str(item) for item in right])})"
    
    def __str__(self):
        return self.fetch

__all__ = [    
    "Row",
    "Rows",
    "Fetch",
]
