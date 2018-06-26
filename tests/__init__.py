"""
    Tests for RUZ API python module

    DANGEROUS: trusted fixtures may be deactivated in few years!
"""

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s "
           "[%(name)s.{%(filename)s}.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%H:%M:%S"
)

__version__ = (2, 1, 2)
