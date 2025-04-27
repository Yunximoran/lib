from functools import wraps


class Catch:
    @staticmethod
    def process(func):
        @wraps(func)
        def wrapper(target, *args, **kwargs):
            if "attribute" in kwargs:
                attribute: dict = kwargs['attribute']
                for opt, val in attribute.items():
                    setattr(target, opt, val)
                del kwargs['attribute']
            try:
                return target(*args, **kwargs)
            except KeyboardInterrupt:
                return False
        return wrapper