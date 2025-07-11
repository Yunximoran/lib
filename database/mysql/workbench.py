from __future__ import annotations


from .connector import Connector
from .dispose import *
from .dispose._exception import NoData, NoSelectDatabase

"""
WorkBench操作层
数据处理层
构造SQL语句
"""
class WorkBench:
    def __init__(self, usedb:str = None):
        self.__conn = Connector(usedb=usedb)
        self.check = Check()
        self.formation = Formation()

    def using(self) -> str:
        """
            ### 查看当前数据库
        """
        return self.__conn.using()
    
    def version(self) -> str:
        """
            ### 查看数据库版本
        """
        return self.__conn.execute("Select Version()")[0]
    
    def tables(self) -> tuple:
        """
            ### 查看当前数据库中的所有表
        """
        usedb = self.__conn.using()
        if usedb is None:
            raise NoSelectDatabase("no selected database")
        return self.__conn.execute(f"select table_name from information_schema.tables where table_schema = '{usedb}'")
    
    def databases(self) -> tuple:
        """
            # 查看所有数据库
        """
        return self.__conn.execute("show databases")
    
    def workbook(self, tbn:str) -> Table:
        """
            ### 工作簿
        
        :param tbn: 工作簿名 <=> MySQL数据表
        :type tbn: str

        """
        return Table(
            tbn=tbn, 
            conn=self.__conn,
            check=self.check,
            formation=self.formation,
            )

    def new(self, dbn:str, exists:bool=False) -> WorkBench:
        """
            ### 创建新的数据库

        :param dbn: 数据库名
        :param exists: 数据库存在时忽略异常

        """
        # print(New(dbn, exists))
        self.__conn.execute("Create DataBase{}{}".format(" if not exists " if exists else " ", dbn))
        return WorkBench(dbn) # 返回一个新的WorkBench
    
    def drop(self, dbn:str, exists:bool=False):
        """
            ### 删除数据库

        :param dbn: 数据库名
        :param exists: 数据库存在时忽略异常

        """
        self.__conn.execute("Drop DataBase{}{}".format(" if not exists " if exists else " ", dbn))

    def create(self, tbn, fetchs, exists=True) -> Table:
        """
            ### 创建新的数据表
        :param tbn: 表名
        :param fetchs: 字段列表
        :param exists: 数据表存在时忽略异常
        """
        self.__conn.execute(Create(tbn, fetchs, exists))
        return self.workbook(tbn)

    def delete(self, tbn, exists=False):                                  # 删除数据表
        self.__conn.execute("Drop DataBase{}{}".format(" if not exists " if exists else " ", tbn)) 
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__conn.close()

    def __str__(self):
        return self.using()



class Table:
    def __init__(
            self, 
            tbn:str, 
            conn:Connector,
            check:Check,
            formation:Formation,
        ):
        """
        :param tbn: 表名
        :param cursor: 游标对象
        :param check:  
        :param formattool:
        :param construction:
        """
        self.__table = tbn
        self.__conn = conn
        self.check = check
        self.formation = formation
        
        self.fields = self.__load_field()

    def __str__(self):
        return self.__table
    

    def __load_field(self):
        results = self.__conn.execute(
            f"select column_name, data_type, column_key from information_schema.columns"
            f" where table_schema='{self.__conn.using()}' and table_name='{self.__table}'"
            f" order by ordinal_position"
        )
        if results:
            num = len(results)  # 列数量
            for field, type, *attrib in results:
                if type == "int":
                    setattr(self, field, Field(field, Int, *attrib))
                    continue
                if type == "float":
                    setattr(self, field, Field(field, Float, *attrib))
                    continue
                if type == "char":
                    setattr(self, field, Field(field, Char, *attrib))
                    continue
                if type == "varchar":
                    setattr(self, field, Field(field, VarChar, *attrib))
                    continue
                if type == "datetime":
                    setattr(self, field, Field(field, DateTime, *attrib))
                    continue
                if type == "date":
                    setattr(self, field, Field(field, Date, *attrib))
                    continue
                if type == "time":
                    setattr(self, field, Field(field, Time, *attrib))
                    continue
    
            # 导出为字典数据
            results = {column_name: (data_type, column_type) for column_name, data_type, column_type in results}
            return results, num
        else: return None
    
    def count(self):
        """
            ### 统计数据条目
        """
        count =  self.__conn.execute(f"Select count(*) from {self.__conn.using()}.{self.__table}")
        if count:
            return count[0]
        else: return None

    def primary(self):
        """
            ### 查询主键
        """
        columns:dict = self.__load_field()[0]
        # print(columns)
        for column in columns.keys():
            if columns[column][-1] == "PRI":
                return column
        return None
    
    def unique(self):
        """
            ### 查询唯一键
        """
        columns:dict = self.__load_field()[0]
        for column in columns.keys():
            if columns[column][-1] == "UNI":
                return column
        return None

    def insert(self, data:Rows|dict, ignore=False):
        """
            执行插入操作

        :param data: 需要插入的数据
        :param ignore: 是否忽略重复值

        """

        # 根据数据类型，执行对应的格式化操作
        if isinstance(data, dict): vals, keys = self.formation.formatDict(data) # 格式化字典数据
        else: vals, keys = self.formation.formatSeries(data)                    # 格式化矩阵数据
        # 格式化方法返回，vals,keys两个变量
        if keys is None and len(vals[0]) != self.__load_field()[-1]: raise NoData("If there is no diameter key, you must insert all columns")
        # Insert(self.__table, vals, keys, ignore=ignore)

        if vals: self.__conn.execute(Insert(self.__table, vals, keys, ignore=ignore))
        else: raise NoData(f'DataError') # 如果vals为空，说明数据存在错误

    def update(self, newData, index=0, condition:Condition=None):
        """
            更新数据

        :param newData: 更新的数据， 字段或者数组， PS: 当数据为数组时, 根据数组长度从表中按顺序获取字段
        :param index: 逐条更新指定索引列, 如果更新的数据包含主键和唯一键优先使用主键, 其次是唯一键, 
        :param condition: 设置批量更新条件
        :type newData: dict|array
        :type index: int
        :type condition: Condition

        
        * 批量更新: 对满足条件的数据进行更新, 执行批量更新时, newData参数只允许传入一维数据
        * 逐条更新: 不设置条件, 从数据中指定某一列作为行索引, 更新其他数据。

        """
        # 格式化数据: 整理成 行数据列表， 字段列表
        if isinstance(newData, dict): 
            vals, keys = self.formation.formatDict(newData)
        else:
            vals, i = self.formation.formatSeries(newData)
            # 更新数据不是字典数据时，按顺序更新数据
            keys = tuple(self.__load_field()[0].keys())[: vals.length]

        # 校验数据
        if vals:
            # 区分更新模式: 逐条更新 | 批量更新
            if condition:
                """
                    设置条件时，使用 data.length 必须 为 1
                    防止条件, 如 id > 1: 重复更新操作导致数据混乱
                """ 
                if len(vals) != 1: raise Exception("批量更新不允许二维数据") 
                iterate = False
            else: iterate = True

            datas:list[dict] = []
            # 二次格式化数据: 整理每行数据对应字段
            for val in vals:
                data = {}
                for key, item in zip(keys, val):
                    data[key] = item
                datas.append(data)
            for data in datas:
                if iterate: # 设置逐条更新索引
                    try:
                        condition = Condition("{} = {}".format(self.primary(), data[self.primary()]))
                    except Exception as e:
                        condition = Condition("{} = {}".format(self.unique(), data[self.unique()]))
                    except Exception as e:
                        condition = Condition("{} = {}".format(*tuple(data.items())[index]))
                self.__conn.execute(Update(self.__table,condition, **data))

        else: raise NoData(f'DataError') # 如果vals为空，说明数据存在错误

    def delete(self, condition=None):
        self.__conn.execute(Delete(self.__table, condition))

    def select(self, findKey=None, condition=None):
        return self.__conn.execute(Select(self.__table, find=findKey, condition=condition))

