from ruz.utils.decorators import abs_none_safe, none_safe

ARGS = (1, 2, None, 4, None)
SAFE_ARGS = (1, 2, 4)
KWARGS = {'a': 1, 'b': 2, 'c': None, 'd': 4, 'e': None}
SAFE_KWARGS = {'a': 1, 'b': 2, 'd': 4}


def func(*args, **kwargs) -> tuple:
    return args, kwargs


@abs_none_safe
def func_abs_none_safe(*args, **kwargs) -> tuple:
    return args, kwargs


@none_safe
def func_none_safe(*args, **kwargs) -> tuple:
    return args, kwargs


def test_func():
    assert func(*ARGS, **KWARGS) == (ARGS, KWARGS)


def test_abs_none_safe():
    assert func_abs_none_safe(*ARGS, **KWARGS) == (SAFE_ARGS, SAFE_KWARGS)


def test_none_safe():
    assert func_none_safe(*ARGS, **KWARGS) == (ARGS, SAFE_KWARGS)
