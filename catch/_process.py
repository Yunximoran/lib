from functools import wraps

from ._catch import __CatchBase, Logger


class _CatchProcess(__CatchBase):
    logger = Logger("process", log_file="process.log")
    
    def process(self, func):
        @wraps(func)
        def wrapper(target, *args, **kwargs):
            if "attribute" in kwargs:
                attribute: dict = kwargs['attribute']
                for opt, val in attribute.items():
                    setattr(target, opt, val)
                del kwargs['attribute']
            try:
                self.record(target)
                return target(*args, **kwargs)
            except KeyboardInterrupt:
                self.record(target, "The Ctrl C", 3)
                return False
        return wrapper
    
    
    
    

