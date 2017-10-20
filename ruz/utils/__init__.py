import os

from ruz.utils.logging import Logger, LEVELS
from ruz.utils.schema import REQUEST_SCHEMA, RESPONSE_SCHEMA, RUZ_API_ENDPOINTS


RUZ_API_URL = "http://92.242.58.221/ruzservice.svc/"
EMAIL_PATTERN = r"\b[a-zA-Z0-9\._-]{2,}@([a-zA-Z]{2,}\.)?[a-zA-Z]{2,}\.ru\b"
