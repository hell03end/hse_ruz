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

__version__ = (2, 0, 1)

# ===== Fixtures =====
TRUSTED_EMAILS = {
    'student': r"dapchelkin@edu.hse.ru",
    'lecturer': r"aromanov@hse.ru"
}
INTRUSTED_EMAILS = {
    'other': r"hell03end@outlook.com",
    'hse': r"hell03end@hse.ru"
}
TRUSTED_GROUP_ID = 7699
TRUSTED_LECTURER_ID = 6232
