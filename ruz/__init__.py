'''
    Python wrapper for HSE RUZ API.

    Usage:
        from ruz import RUZ

        api = RUZ()
        assert api.v == 1
        assert api.schedule("mymail@edu.hse.ru")
'''

import os

from .RUZ import RUZ
from .utils import REQUEST_SCHEMA, RESPONSE_SCHEMA

__author__ = "hell03end"
__version__ = (0, 1, 0)
__all__ = ("RUZ", "REQUEST_SCHEMA", "RESPONSE_SCHEMA")
