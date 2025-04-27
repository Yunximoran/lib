import re 
import logging

from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path

from ..init.resolver import __resolver

levelnode = __resolver("default", "log-settings", "level", is_node=True)

#  读取默认日志级别
if re.match(r"^(0|d|(debug))$", levelnode.data.lower()):
    level = logging.INFO
elif re.match(r"^(1|i|(info))$", levelnode.data.lower()):
    level = logging.INFO
elif re.match(r"^(2|w|(warning))$", levelnode.data.lower()):
    level = logging.WARNING
elif re.match(r"^(3|e|(error))$", levelnode.data.lower()):
    level = logging.INFO
elif re.match(r"^(4|c|(critical))$", levelnode.data.lower()):
    level = logging.CRITICAL
else:
    raise KeyError(f"Invalid log settings {levelnode.tag}: {levelnode.data}, address:{levelnode.addr}")


WROKDIR = Path.cwd()                            # 工作目录
LOGDIR = WROKDIR.joinpath("logs")               # 输出目录
ENCODING = __resolver("default", "encoding")    # 编码格式

# 创建输出目录
LOGDIR.mkdir(parents=True, exist_ok=True)

class Logger:
    # 日志管理器只在despose中使用吗？
    def __init__(self, name, log_file='.log', level=level,*,
                 log_path:Path=LOGDIR,
                 max_bytes=5*1024*1024,
                 backup_count=5,
                 console=False,
                 ):
        """
            # 日志管理

        :param name: 日志记录器名称
        :param log_file: 日志文件名
        :param level: 日志级别
        :param max_bytes: 单个日志文件最大字节数
        :param backup_count: 保留的备份文件数量
        :param console: 是否再控制台输出
        :type name: str
        :type log_file: str
        :type level: int
        :type max_bytes: int
        :type backup_count: int
        :type console: bool
        """
        # 创建日志目录（如果不存在）
        if not isinstance(log_path, Path):
            log_path = Path(log_path)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # 创建日志文件 (如果文件不存在)
        self.file_path = log_path.joinpath(log_file)
        self.file_path.touch()
        
        # 初始化logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 创建日志格式器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 是否需要控制台输出
        if console:
            self.addconsole(formatter)
        # 创建滚动文件处理器
        self.rotating(formatter, max_bytes, backup_count)
    
    def addconsole(self, formatter):
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def rotating(self, formatter, maxbytes, backup):
        file_handler = RotatingFileHandler(
            self.file_path,
            mode="a",
            maxBytes=maxbytes,
            backupCount=backup,
            encoding=ENCODING,
            delay=True
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def format_logtext(self, *msgs, **dmsgs):
        """
            格式化日志文本

        :param *msgs:
        :param **dmsgs:
        """
        logtext = []
        logtext.append("\t".join(msgs))
        
        for msg in dmsgs:
            item = f"{msg}: {dmsgs[msg]}"
            logtext.append(item)
        return "\n".join(logtext)
    
    def record(self, level:int , *msgs, **kwmsgs):
        """
        日志记录器：执行写入操作

        :param level: 记录等级
        :param msg: 日志信息
        :type level: int
        :type msg: str

        log level: debug < info < waring < error < critical
        """
        logtext = self.format_logtext(*msgs, **kwmsgs)

        if level == 0:
            self.__debug(logtext)
        elif level == 1:
            self.__info(logtext)
        elif level == 2:
            self.__warning(logtext)
        elif level == 3:
            self.__error(logtext)
        elif level == 4:
            self.__critical(logtext)
        else:
            raise ValueError("must range 0, 4 the attribute level")
    
    def __debug(self, message):
        self.logger.debug(message)
    
    def __info(self, message):
        self.logger.info(message)
    
    def __warning(self, message):
        self.logger.warning(message)
    
    def __error(self, message):
        self.logger.error(message)
    
    def __critical(self, message):
        self.logger.critical(message)
        


if __name__ == "__main__":
    logger = Logger("logtext", log_file="logtext.log")
    logtext = logger.format_logtext("t1", "t2", a1 = __file__, a2 = __name__)
    print(logtext)
    logger.record(4, "hello wrold")