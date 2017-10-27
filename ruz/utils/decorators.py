from collections import Callable
from functools import wraps


def abs_none_safe(func: Callable) -> Callable:
    """
        Absolute None safe decorator

        Pass only not None kwargs and also args to function (no None at all)

        :param func, required - wrapped function/method.

        Usage
        -----
        @abs_none_safe
        def some_func(*args, **kwargs):
            pass  # all None args/kwargs will be filtered
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> object:
        params = []
        for arg in args:
            if arg is not None:
                params.append(arg)
        param_dict = {}
        for key, value in kwargs.items():
            if value is not None:
                param_dict[key] = value
        result = func(*params, **param_dict)
        return result
    wrapper.__doc__ = func.__doc__
    return wrapper


def none_safe(func: Callable) -> Callable:
    """
        Pass only not None kwargs to function (args can be None)

        :param func, required - wrapped function/method.

        Usage
        -----
        @none_safe
        def some_func(*args, **kwargs):
            pass  # only not None kwargs will be passed
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> object:
        param_dict = {}
        for key, value in kwargs.items():
            if value is not None:
                param_dict[key] = value
        result = func(*args, **param_dict)
        return result
    wrapper.__doc__ = func.__doc__
    return wrapper
