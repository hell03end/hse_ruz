import os
from collections import Callable
from functools import wraps


# ===== Constants =====

RUZ_API_URL = os.environ.get("RUZ_API_URL",
                             r"http://92.242.58.221/ruzservice.svc/")

# detect RUZ API version from possible RUZ API URLs
RUZ_API_V = 1
if RUZ_API_URL == r"http://92.242.58.221/ruzservice.svc/v2/":
    RUZ_API_V = 2
elif RUZ_API_URL == r"https://www.hse.ru/api/":
    RUZ_API_V = 3

# default values
CHECK_EMAIL_ONLINE = bool(os.environ.get("CHECK_EMAIL_ONLINE", False))
USE_NONE_SAFE_VALUES = bool(os.environ.get("USE_NONE_SAFE_VALUES", True))


# ===== Decorators =====

def none_safe(args: bool=True, kwargs: bool=True) -> Callable:
    """ Pass only not None args/kwargs to function """
    def decor(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*_args, **_kwargs) -> object:
            if args:
                _args = [arg for arg in _args if arg is not None]
            if kwargs:
                _kwargs = {k: v for k, v in _kwargs.items() if v is not None}
            return func(*_args, **_kwargs)
        return wrapper
    return decor
