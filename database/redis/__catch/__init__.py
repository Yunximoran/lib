from functools import wraps


class Catch:
    @staticmethod
    def ping(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try: return func(*args, **kwargs)
            except ConnectionError: return False
        return wrapper