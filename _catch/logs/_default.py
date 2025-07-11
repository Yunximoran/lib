import re, logging
from pathlib import Path

from ..._init import _resolver
from logging import (
    StreamHandler,
    FileHandler,
    NullHandler
)
from logging.handlers import (
    QueueHandler,
    MemoryHandler,
    SocketHandler,
    SysLogHandler,
    HTTPHandler,
    DatagramHandler,
    NTEventLogHandler,
    WatchedFileHandler,
    RotatingFileHandler,
    TimedRotatingFileHandler,
    SMTPHandler,
)
from .._execption import (
    ConfigOptionsIsNoFound
)

class _Logger:
    _conf = _resolver("log-settings")
    encoding = _resolver("default", "encoding")
    log_path = Path(__file__).parent
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        log_file = self.log_path.joinpath("{}.log".format(name))
        log_file.touch(exist_ok=True)

        self._set_level_()
        self._set_console_(formatter)
        self._set_handler_(log_file, formatter)

    def _set_console_(self, formatter):                        # 设置终端输出
        is_console = self._conf.search("console").data
        if is_console:
            console_handler = StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def _set_handler_(self, log_file, formatter):              # 设置日志处理器
        _conf_handler = self._conf.search("handler")
        if _conf_handler is not None:
            type = _conf_handler["type"]
            if type == FileHandler.__name__:                # 文件处理器： 输出日志到文件
                mode = _conf_handler.search("mode").data
                delay = _conf_handler.search("delay").data
                handler = FileHandler(
                    log_file,
                    mode=mode,
                    encoding=self.encoding,
                    delay=delay,
                )
            elif type == NullHandler.__name__:              # 异常处理器： 不对错误消息进行记录
                handler = NullHandler()
            elif type == QueueHandler.__name__:             # 队列处理器： 输出日志到队列
                handler = QueueHandler()
            elif type == MemoryHandler.__name__:            # 缓存处理器： 输出日志到缓存区
                capaity=_conf_handler.search("capaity").data
                flushLevel=_conf_handler.search("flusLevel").data
                target=_conf_handler.search("target").data
                flushOnClose=_conf_handler.search("flushOnClose").data
                handler = MemoryHandler(
                    capacity=capaity,
                    flushLevel=flushLevel,
                    target=target,
                    flushOnClose=flushOnClose
                )
            elif type == SocketHandler.__name__:            # Socket处理器: 输出日志到TCP/IP
                handler = SocketHandler()
            elif type == SysLogHandler.__name__:            # 系统日志处理器： 输出日志到Unix syslog 守护进程
                handler = SysLogHandler()
            elif type == HTTPHandler.__name__:              # URL请求处理器： 输出日志到HTTP服务器
                type = HTTPHandler()
            elif type == DatagramHandler.__name__:          # Socket处理器：输出日志到UDP
                handler = DatagramHandler()
            elif type == SMTPHandler.__name__:              # 邮件处理器： 输出日志到邮件
                handler = SMTPHandler()
            elif type == NTEventLogHandler.__name__:        # NT事件处理器：输出日志到 Windows NT/2000/XP 事件日志
                handler = NTEventLogHandler()
            elif type == WatchedFileHandler.__name__:       # 监视处理器： 监视要写入的文件，仅在Unix中有效
                handler = WatchedFileHandler()
            elif type == RotatingFileHandler.__name__:      # 轮转日志处理(基于文件大小轮转)
                mode = _conf_handler.search("mode").data
                maxbytes = _conf_handler.search("max-bytes").data
                backup = _conf_handler.search("backup").data
                delay = _conf_handler.search("delay").data
                handler = RotatingFileHandler(
                    log_file,
                    mode=mode,
                    maxBytes=maxbytes,
                    backupCount=backup,
                    encoding=self.encoding,
                    delay=delay,
                )
            elif type == TimedRotatingFileHandler.__name__: # 轮转日志处理(基于时间日期轮转)
                when = _conf_handler.search("when").data
                interval = _conf_handler.search("interval").data
                backup = _conf_handler.search("backup").data
                delay = _conf_handler.search("delay").data
                utc = _conf_handler.search("utc").data
                atTime = _conf_handler.search("atTime").data

                handler = TimedRotatingFileHandler(
                    log_file,
                    when=when,
                    interval=interval,
                    backupCount=backup,
                    encoding=self.encoding,
                    delay=delay,
                    utc=utc,
                    atTime=atTime,
                )
            else: raise TypeError("logger handler error, not type {}".format(type(handler)))

            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        else:
            raise ConfigOptionsIsNoFound("option: handler is not found")

    def _set_level_(self):                                     # 设置日志等级
        level = self._conf.search("level").data.lower()
        if re.match(r"^(0|d|(debug))$", level):
            self.logger.setLevel(logging.DEBUG)
        elif re.match(r"^(1|i|(info))$", level):
            self.logger.setLevel(logging.INFO)
        elif re.match(r"^(2|w|(warning))$", level):
            self.logger.setLevel(logging.WARNING)
        elif re.match(r"^(3|e|(error))$", level):
            self.logger.setLevel(logging.ERROR)
        elif re.match(r"^(4|c|(critical))$", level):
            self.logger.setLevel(logging.CRITICAL)
        else:
            raise KeyError(f"Invalid log level settings {level}")
        
    def logtext(self, text, *msgs, **dmsgs):                   # 日志文本格式化工具
        logtext = []
        logtext.append(" ".join([msg if isinstance(msg, str) else str(msg) for msg in msgs]))

        for msg in dmsgs:
            val = dmsgs[msg]
            if not isinstance(msg, str):
                msg = str(msg)
            if not isinstance(val, str):
                val = str(val)

            logtext.append("{}: {}".format(msg, val))

        return "{}\n{}\n".format(text, "\n".join(logtext))
    
    def record(self, level:int, text:str, *msgs, **dmsgs):     # 记录器
        """
        :param level: 日志等级
        :param text: 描述文本
        :param msgs: 额外参数
        :param dmsgs: 带标题的额外参数

        :type level: int
        :type text: str
        """
        logtext = self.logtext(text, *msgs, **dmsgs)

        if level == 0: self.logger.debug(logtext);    return text
        if level == 1: self.logger.info(logtext);     return text
        if level == 2: self.logger.warning(logtext);  return text
        if level == 3: self.logger.error(logtext);    return text
        if level == 4: self.logger.critical(logtext); return text
        raise KeyError("the level must int and val in [0, 4] -> debug(0)、 info(1)、 waring(2)、 error(3)、 critical(4)")
        

