import re
import os
import zipfile
import tarfile
from getpass import getpass
from ._base import _BaseSystem
from pathlib import Path


class Linux(_BaseSystem):
    def __init__(self):
        super().__init__()
        self._disks = [Path("/")]
        
    # 用户权限
    def close(self):
        return self.executor(["sudo", "shutdown", "now"], isadmin=True)
    
    def restart(self):
        return self.executor(["sudo", "shutdown", "-r"], isadmin=True)
        
    def start_software(self, path):
        path = self._path_(path)
        report = self.executor(f"./{path.name}", cwd=path.parent, iswait=False)
        return report
    
    def close_software(self, software):
        path = self._path_(software)
        processes = self.check_soft_status(path)
        for process in processes:
            process.kill()
    
    def compress(self, topath, frompath, mode=None):
        """
            压缩
        """
        topath = self._path_(topath, check=True)
        frompath = self._path_(frompath, check=True)
        
        if not frompath.is_dir():
            raise Exception(f"{frompath} must a dir")  
        
        if mode is not None:
            if mode == "gz":
                suffix = "gz"
            elif mode == "bz2":
                suffix = "bz"
            elif mode == "xz":
                suffix = "lxma"
            else:
                raise "模式错误"
            mode = ":".join(("w", mode))
            packname = ".".join((frompath.name, "tar", suffix))
        else:
            mode = "w"
            packname = ".".join((frompath.name, "tar"))
                
        
        topath = topath.joinpath(packname)
        with tarfile.open(topath, mode=mode) as tar:
            tar.add(frompath, arcname=frompath.parent)

    def uncompress(self, topath, frompath, clear=False):
        """
            解压缩
        pack 文件地址
        to: 保存位置
        """
        topath, frompath = super().uncompress(topath, frompath, (r".tar", r".gz", r".bz", r".lxma"))
        
        with tarfile.open(frompath, "r:*") as tar:
            tar.extractall(topath)

        if clear:
            frompath.unlink()
        
    def wget(self, url, path=None):
        # 网络请求
        return super().wget(url, path)
    
    def remove(self, path, *, isdir=False):
        return self.executor(\
            ["rm", path] if not isdir else ["rm", "-D", path]
            )
    
    def move(self, topath, frompath):
        return self.executor(["mv", topath, frompath])
    
    def build_hyperlink(self, topath:Path, frompath:Path):
        topath = self._path_(topath)
        frompath = self._path_(frompath)
        if not frompath.exists():
            raise "source file is not exists"
        
        if topath.exists():
            topath.unlink()
            
        topath = str(topath)
        frompath = str(frompath)
        report = self.executor(["ln", "-s", frompath, topath])
        return topath, report
        


    def executor(self, args, isadmin=False, *, cwd=None, iswait=True) -> str:
        """
            args: 指令参数
            label: 软件名
            isdamin: 是否需要管理员权限
        """
        # 格式化为shell字符串
        if isinstance(args, list):
            args = " ".join(map(str, args))

        if isadmin or re.match("^(sudo)", args):
            # 升级为管理员shell，并设置为从标准输入获取密码
            args = self.__uproot(args)
            password = self._conf.password
        else:
            password = None

        msg, err = super().executor(args, cwd=cwd,stdin=password, timeout=10, iswait=iswait)

        if err:
            self.record(3, f"exec {args} results:\n{err}")
        else:
            self.record(1, f"exec {args} results:\n{msg}")
        return  self.report(args, msg, err)\
        if not re.match("[(权限)|(password)|(密码)]", f"{err}")\
        else self.executor(args, True)
    
    def __uproot(self, args:str) -> str:                         # 升级指令权限
        if not re.match(r"^(sudo)(\s(-S))", args) \
            and re.match(r"^(sudo)", args):
            # -S， 读取标准输入密码
            args = args.replace(r"sudo", "sudo -S")
        else:
            if not re.match(r"^(sudo)(\s(-S))", args):
                args = " ".join(map(str, ["sudo -S", args]))
        return args