import os

from ruz.utils.decorators import none_safe
from ruz.utils.logging import Logger, log
from ruz.utils.schema import (REQUEST_SCHEMA, RESPONSE_SCHEMA,
                              RUZ_API_ENDPOINTS, RUZ_API2_ENDPOINTS)


RUZ_API_URL = r"http://92.242.58.221/ruzservice.svc/"
RUZ_API2_URL = r"https://www.hse.ru/api/"
EMAIL_PATTERN = r"\b[a-zA-Z0-9\._-]{2,}@([a-zA-Z]{2,}\.)?[a-zA-Z]{2,}\.ru\b"
EMAIL_DOMAINS = (r"hse.ru", r"edu.hse.ru")
