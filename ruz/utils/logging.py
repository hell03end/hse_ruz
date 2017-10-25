import logging
from collections import Callable
from functools import wraps


def Logger(name: str, level: int=logging.INFO, **kwargs) -> logging.RootLogger:
    logging.basicConfig(
        format=kwargs.pop(
            "format",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ),
        level=level
    )
    return logging.getLogger(name)


def log(func: Callable, level: int=logging.DEBUG, **kwargs) -> Callable:
    """ Log function entering, arguments and exiting (to debug) """
    logger = Logger(
        "{}::{}".format(func.__module__, func.__name__),
        level,
        **kwargs
    )
    with_args = kwargs.pop("with_args", True)

    @wraps(func)
    def wrapper(*args, **kwargs) -> object:
        logger.debug("Entering: %s", func.__name__)
        if with_args:
            for arg in args:
                logger.debug(arg)
            for key, value in kwargs.items():
                logger.debug("%s = %s", key, value)
        result = func(*args, **kwargs)
        logger.debug("Exiting: %s", func.__name__)
        return result
    return wrapper
