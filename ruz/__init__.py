'''
    Python wrapper for HSE RUZ API.

    Usage:
        from ruz import RUZ

        api = RUZ()
        assert api.v == 1
        assert api.schedule("mymail@edu.hse.ru")
'''

import os

from ruz.RUZ import RUZ
from ruz.utils import REQUEST_SCHEMA, RESPONSE_SCHEMA, EMAIL_DOMAINS

__author__ = "hell03end"
__version__ = (0, 2, 1)
__all__ = ("RUZ", "REQUEST_SCHEMA", "RESPONSE_SCHEMA")
