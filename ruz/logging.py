import logging
import os
from collections import Callable
from functools import wraps

ENABLE_LOGGING = os.environ.get("HSE_RUZ_ENABLE_LOGGING", True)


def log(func: Callable) -> Callable:
    if not ENABLE_LOGGING:
        return func

    @wraps(func)
    def wrapper(*args, **kwargs) -> object:
        func_name = func.__name__
        logging.debug("[%s]\tENTER", func_name)
        for arg in args:
            logging.debug("[%s]\tARG\t%s", func_name, arg)
        for key, value in kwargs.items():
            logging.debug("[%s]\tKWARG\t%s=%s", func_name, key, value)
        result = func(*args, **kwargs)
        logging.debug("[%s]\tEXIT", func_name)
        return result
    return wrapper
