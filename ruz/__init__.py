import os

from .utils import RUZ_API_ENDPOINTS, RUZ_API_URL
from .RUZ import RUZ


__doc__ = open(os.path.join(os.path.dirname(__file__), "README.md"),
               encoding="utf-8", errors="xmlcharrefreplace").read()
__author__ = "hell03end"
__version__ = (0, 0, 1)
__all__ = ("RUZ")
