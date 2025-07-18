from functools import partial
from multiprocessing import Process as _Process
from multiprocessing.pool import Pool as _Pool
from multiprocessing import (
    Lock,
    Queue,
    Value,
    Event
)

from .._catch import _Catch, _Logger
from .._init import _resolver

class Task:
    logger = _Logger("process")
    catch = _Catch(logger)
    def __init__(self):
        pass

    @catch.Process
    def __call__(self, target, *args, **kwargs):
        return target   
    
    def stdout(self, msg):
        return msg

    def stderr(self, err):
        return err
    


class Pool(_Pool):
    task = Task()
    
    _conf = _resolver("preformance")
    _min_processes = _conf.search("min-processes").data
    _max_processes = _conf.search("max-processes").data

    def __init__(self, processes = None, initializer = None, initargs = (), maxtasksperchild = None, context = None):
        """
            初始化进程池
        定义进程数范围
        """
        if processes is None or processes < 5:
            processes = self._min_processes 
        elif processes > 10:
            processes = self._max_processes
        super().__init__(processes, initializer, initargs, maxtasksperchild, context)
        
    def map_async(self, func, iterable, *, attribute={}, chunksize = None, callback = task.stdout, error_callback = task.stderr):
        # 包装工作函数， 添加多进程异常捕获， 设置特定情况下函数缺失属性
        worker = partial(self.task, func, attribute=attribute)
        return super().map_async(worker, iterable, chunksize, callback, error_callback)

    def apply_async(self, func, args=(), kwds={}, *, attribute={}, callback = task.stdout, error_callback = task.stderr):
        # 包装工作函数， 添加多进程异常捕获， 设置特定情况下函数缺失属性
        worker = partial(self.task, func, attribute=attribute)
        return super().apply_async(worker, args, kwds, callback, error_callback)

    def join(self):
        try:
            super().join()
        except KeyboardInterrupt:
            self.terminate()
            super().join()

    

class Process(_Process):
    task = Task()
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, attribute={}, daemon = None):
        super().__init__(group, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._target = partial(self.task, target, attribute=attribute)
    
    def join(self, timeout = None):
        try:
            super().join(timeout) 
        except KeyboardInterrupt:
            self.terminate()
            super().join(timeout)