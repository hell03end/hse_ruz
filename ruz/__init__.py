'''
    Python wrapper for HSE RUZ API.

    Usage:
        from ruz import RUZ

        api = RUZ()
        assert api.v == 2
        assert api.get("buildings")
'''

import os

from .utils import RUZ_API_ENDPOINTS, RUZ_API_URL
from .RUZ import RUZ


__author__ = "hell03end"
__version__ = (0, 1, 0)
__all__ = ("RUZ")
