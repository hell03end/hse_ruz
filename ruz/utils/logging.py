import logging
from collections import Callable
from functools import wraps


def Logger(name: str, level: int=logging.INFO, **kwargs) -> logging.RootLogger:
    """
        Creates configured logger

        :param name, required - name for logger.
        :param level - logging level.
        :param format, str - logging format.

        Usage
        -----
        logger = Logger(__name__)

        >>> Logger("some name").info("Hello, world!")
        ... - some name - INFO - Hello, world!
        >>> Logger()
        Traceback (most recent call last):
            ...
        TypeError: Logger() missing 1 required positional argument: 'name'
        >>> Logger(123)
        Traceback (most recent call last):
            ...
        ValueError: Expect str, got: <class 'int'>
    """
    if not isinstance(name, str):
        raise ValueError("Expect str, got: {}".format(type(name)))
    logging.basicConfig(
        format=kwargs.pop(
            "format",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ),
        level=level
    )
    return logging.getLogger(name)


def log(func: Callable) -> Callable:
    """
        Log function entering, arguments and exiting (to debug)

        :param func, required - wrapped function/method.

        Usage
        -----
        @log
        def some_func():
            pass
    """
    logger = Logger(
        name="{}::{}".format(func.__module__, func.__name__),
        level=logging.DEBUG
    )

    @wraps(func)
    def wrapper(*args, **kwargs) -> object:
        logger.debug("Entering: %s", func.__name__)
        for arg in args:
            logger.debug("arg::%s", arg)
        for key, value in kwargs.items():
            logger.debug("kwarg::%s=%s", key, value)
        result = func(*args, **kwargs)
        logger.debug("Exiting: %s", func.__name__)
        return result
    wrapper.__doc__ = func.__doc__
    return wrapper


if __name__ == "__main__":
    import doctest
    doctest.testmod()
