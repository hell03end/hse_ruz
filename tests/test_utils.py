from ruz.utils.decorators import abs_none_safe, none_safe
from ruz.utils.logging import log

ARGS = (1, 2, None, 4, None)
SAFE_ARGS = (1, 2, 4)
KWARGS = {'a': 1, 'b': 2, 'c': None, 'd': 4, 'e': None}
SAFE_KWARGS = {'a': 1, 'b': 2, 'd': 4}


@log
def func_log(*args, **kwargs) -> tuple:
    """ Fixture for test_log """
    return args, kwargs


@abs_none_safe
def func_abs_none_safe(*args, **kwargs) -> tuple:
    """ Fixture for test_abs_none_safe """
    return args, kwargs


@none_safe
def func_none_safe(*args, **kwargs) -> tuple:
    """ Fixture for test_none_safe """
    return args, kwargs


def test_log():
    assert func_log(*ARGS, **KWARGS) == (ARGS, KWARGS)
    assert func_log.__doc__ == " Fixture for test_log "


def test_abs_none_safe():
    assert func_abs_none_safe(*ARGS, **KWARGS) == (SAFE_ARGS, SAFE_KWARGS)
    assert func_abs_none_safe.__doc__ == " Fixture for test_abs_none_safe "


def test_none_safe():
    assert func_none_safe(*ARGS, **KWARGS) == (ARGS, SAFE_KWARGS)
    assert func_none_safe.__doc__ == " Fixture for test_none_safe "
