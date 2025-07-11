import os
import time
import subprocess
import platform
import socket
import uuid
import re
import inspect
import sys
import ctypes
import json
import string
import zipfile,tarfile
from typing import List
from pathlib import Path
from collections.abc import Iterable
from xml.etree import ElementTree as et
from typing import Tuple
import psutil
from typing import Generator
from psutil import NoSuchProcess, AccessDenied

from ..._catch import _Catch, _Logger
from ..._catch import CatchSystemEvent as catch_event
from ..._init import _resolver

class _BaseSystem:
    # 获取工作目录
    logger = _Logger("system")
    catch = _Catch(logger)
    _disks = []

    _conf = _resolver("system")
    Name = _conf.search("name").data
    Version = _conf.search("version").data
    Machine = _conf.search("machine").data
    OS = _conf.search("OS").data
    CPU = _conf.search("CPU").data
    RAM = _conf.search("RAM").data
    CWDIR = Path.cwd()

    def __init__(self):
        if int(self._conf["uuid"]) != uuid.getnode():
            self._conf["uuid"] = uuid.getnode()
            self._config_update_()
    
    def _config_update_(self):
        self.logger.record(1, "update system infomation")
        self._conf.search("name").setdata(platform.node())
        self._conf.search("release").setdata(platform.release())
        self._conf.search("version").setdata(platform.version())
        self._conf.search("machine").setdata(platform.machine())
        self._conf.search("OS").setdata(platform.system())
        self._conf.search("CPU").setdata(platform.processor())

        RAM = psutil.virtual_memory().total / (1024 ** 3)
        self._conf.search("RAM").setdata(round(RAM, 2))
        _resolver.save()
        sys.exit(1)

    # def _up_data_()
    @catch.System(catch_event.PROCESS)
    def _check_process_status_(self, path:Path, process:psutil.Process) -> List[psutil.Process]:
        """
            检查进程状态
        """
        current_process = Path(process.exe())
        if re.match(path.stem, process.name()):
            # 进程路径包含软件名
            exe_depend_path = [parent_process.exe() for parent_process in process.parents()] # [Process(parent).exe for parent in process.parents()]
            exe_depend_path.append(process)
            if str(path) in exe_depend_path:
                return process
            else:
                return None
        if path.parent in current_process.parents:
            # 需要区别单文件可执行程序
            return process
    
        
    def check_soft_status(self, path, *, pid=None) -> List[psutil.Process]:  # 遍历系统进程池
        """
        :param path: 检索目标进程路径
        :param pid: 检索目标进程PID
        """
        path = self._path_(path)
        processes = []
        for process in psutil.process_iter():
            # 匹配项目
            checked_process = self._check_process_status_(path, process)
            if checked_process:
                processes.append(checked_process)
        return processes
    
    def _path_(self, path:str|Path, *,                                       # 路径转换
              check=False
              ) -> Path:
        if isinstance(path, str):
            path = Path(path)
            
        if check and not path.exists():
            raise FileExistsError(f"{path} is not exists")
        return path
    
    def checkfile(self, check_object, path=None, base=None):    # 查找文件
        
        """
            # 查找文件
        check_object: 查找对象
        path: 文件目录
        base: 查找目录
        """
        if base is not None:
            if not isinstance(base, Path):
                base = Path(base)
            if not base.exists():
                raise "check dir is not exists"
        else:
            base = self._disks
        
        if path:
            # 如果不是Path转化为Path
            if not isinstance(path, Path):
                path = Path(path)
            # 如果路径本地本地存在方法它， 校验路径是否存在
            if path.exists():
                return path
        else:
            results: List[Path] = []
            for disk in self._disks:
                for root, dirs, files in os.walk(disk):
                    for file in files:
                        if file == check_object:
                            results.append(os.path.join(root, file))
                    for dir in dirs:
                        if dir == check_object:
                            results.append(os.path.join(root, dir))     
            return results
    
                
    def executor(self, args, *,                 # shell执行器
                 cwd:Path=None,
                 stdin: str=None,
                 timeout:int=None,
                 iswait:bool=True
                 ):
        """
        :param args: 封装的shell指令列表
        :param cwd: 指定工作目录
        :param stdin: 设置输出流
        :param timeout: 设置超时时间
        :param iswait: 设置是否等待进程结束

        :type args: tuple
        :type cwd: path
        :type stdin: str
        :type timeout: int
        :type iswait: bool

        :return report: 返回报文, 用于向服务端汇报执行结果
        """
        process= subprocess.Popen(
                args=args,
                shell=True, 
                text=True,
                stdin = subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
            )
        if iswait:
            msg, err = process.communicate(input=stdin, timeout=timeout)
        else:
            if process.poll() is None:
                msg, err = True, False
            else:
                msg, err = False, True
        return msg, err
    
    def formatparams(self, typecode:int, data: dict|list) -> str:  # 预定义表单类型
        """
        0: instruct,
        1: software,
        2: report,
        3: download
        """
        types = [
            "instruct",
            "software",
            "report",
            "download"
        ]
        return json.dumps({
            "type": types[typecode],
            "data": data,    # 携带的data， 软件路径列表 | 错误报文
            "cookie": time.time()
        }, ensure_ascii=False)     

    @catch.JSON("execute report")
    def report(self, args, msg, err): # 格式化报文
        return json.dumps({
            "status": "ok" if not err else "error",
            "instruct": " ".join([param if isinstance(param, str) else str(param) for param in args]) if isinstance(args, Iterable) else args,
            "msg": str(msg) if msg else "<No output>",
            "err": str(err) if err else "<No error output>",
            "time": time.time()
        }, ensure_ascii=False, indent=4)   
    
        
    def init(self):
        pass
    
    # 硬件相关
    def close(self):# 关机
        pass
    
    def restart(self):# 重启
        pass
    
    
    # 软件相关
    def start_software(self, path): # 启动软件
        pass
    
    def close_software(self, softname): # 关闭软件
        pass
    
    # 文件相关
    def compress(self, topath, frompath, mode):
        # 压缩
        pass
    
    def uncompress(self, topath, frompath, suffix):
        topath = self._path_(topath, check=True)
        frompath = self._path_(frompath, check=True)
        
        if frompath.suffix not in suffix:
            raise Exception(f"source must in {suffix}, actually gives: {frompath}")
        
        packname = frompath.name.split(".")[0] 
        topath = topath.joinpath(packname)
        topath.mkdir(exist_ok=True)
        return topath, frompath
    
    def wget(self, url, path=None):
        # 下载
        pass
    
    def remove(self, path):
        # 移动文件或删除
        pass
            

    def build_hyperlink(self, alias, frompath):
        pass
    
    def __uproot(self):
        # 升级root权限
        pass
    
    def record(self, level:int, msg):
        self.logger.record(level, msg)


# class Information:
#     # 本机信息
#     NODE = platform.node()
#     OS = platform.system()
#     VERSION = platform.version()
#     MACHINE = platform.machine()
#     RAM = psutil.virtual_memory().total / (1024 ** 3)

#     # CPU信息
#     PROCESSOR = platform.processor()
#     PHYSICALCORES = psutil.cpu_count(logical=False)
#     LOGICALCORES = psutil.cpu_count(logical=True)
#     ARCHITECTURE = platform.architecture()[0]