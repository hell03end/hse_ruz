import json
import logging
import os
import re
from collections import Callable
from datetime import datetime, timedelta
from functools import wraps
from urllib import error, parse, request

from ruz.logging import log
from ruz.schema import API_ENDPOINTS, API_URL, REQUEST_SCHEMA

CHECK_EMAIL_ONLINE = bool(os.environ.get("CHECK_EMAIL_ONLINE", False))
USE_NONE_SAFE_VALUES = bool(os.environ.get("USE_NONE_SAFE_VALUES", True))
HSE_EMAIL_REGEX = re.compile(r"^[a-z0-9\._-]{3,}@(edu\.)?hse\.ru$")


def none_safe(func: Callable) -> Callable:
    """ Pass only not None args/kwargs to function """
    @wraps(func)
    def wrapper(*args, **kwargs) -> object:
        args = [arg for arg in args if arg is not None]
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return func(*args, **kwargs)
    return wrapper


def is_student(email: str) -> bool or None:
    """
        Check email belongs to student

        :param email, required - valid HSE email addres or domain.

        Stutent's domain:   @edu.hse.ru
        HSE stuff' domain:  @hse.ru
    """
    email_domain = email.lower().split("@")[-1]

    if email_domain == "edu.hse.ru":
        return True
    elif email_domain == "hse.ru":
        return False

    logging.debug("Wrong HSE email domain: '%s'", email_domain)


def is_hse_email(email: str) -> bool:
    """
        Check email is valid HSE corp. email

        :param email, required - email address to check.
    """
    if HSE_EMAIL_REGEX.fullmatch(email.lower()):
        return True
    logging.debug("Incorrect HSE email '%s'.", email)
    return False


def get_formated_date(day_bias: int or float=0) -> str:
    """
        Return date in RUZ API compatible format

        :param day_bias - number of day from now.
    """
    return (datetime.now() + timedelta(
        days=float(day_bias)
    )).strftime("%Y.%m.%d")


@log
def is_valid_hse_email(email: str) -> bool:
    """
        Check email is valid via API endpoint call (schedule)

        :param email - email address to check (for schedules only).
    """
    @none_safe
    def request_schedule_api(**params) -> list or dict:
        return request.urlopen(make_url(
            "schedule",
            email=email,
            fromDate=get_formated_date(),
            toDate=get_formated_date(1),
            **params
        ))

    email = email.strip().lower()
    if not is_hse_email(email):
        return False

    try:
        response = request_schedule_api(
            receiverType=1 if not is_student(email) else None
        )
        del response
    except (error.HTTPError, error.URLError) as err:
        logging.debug("Email '%s' wasn't verified.\n%s", email, err)
        return False
    return True


@log
def is_valid_schema(endpoint: str,
                    check_email_online: bool=CHECK_EMAIL_ONLINE,
                    **params) -> bool:
    """
        Check params fit schema for certain endpoint

        :param endpoint - endpoint for request.
        :param check_email_online - use is_valid_hse_email.
        :param params - schema params.
    """

    if (endpoint == "schedule" and "lecturerOid" not in params and
            "studentOid" not in params and "email" not in params and
            "auditoriumOid" not in params):
        logging.debug("One of the followed required: lecturer_id, "
                      "auditorium_id, student_id, email for "
                      "schedule endpoint.")
        return False

    if params.get('email') is not None:
        email = params['email']
        if not is_hse_email(email):
            del email
            return False
        elif check_email_online and not is_valid_hse_email(email):
            logging.debug("'%s' is not verified by API call.", email)
        del email

    endpoint = API_ENDPOINTS.get(endpoint)
    if endpoint is None:
        logging.debug("Can't find endpoint: '%s'.", endpoint)
        del endpoint
        return False

    schema = REQUEST_SCHEMA[endpoint]
    for key, value in params.items():
        if key not in schema:
            logging.debug("Can't find '%s' schema param: '%s'", endpoint, key)
            del schema, endpoint
            return False
        if not isinstance(value, schema[key]):
            logging.debug("Expected {} for '{}'::'{}' got: {}",
                          schema[key], endpoint, key, type(value))
            del schema, endpoint
            return False
    del schema, endpoint
    return True


@log
def make_url(endpoint: str, **params) -> str:
    """
        Creates URL for API requests

        :param endpoint - endpoint for request.
        :param params - request params.
    """
    url = "".join((API_URL, API_ENDPOINTS[endpoint]))
    if params:
        return "?".join((url, parse.urlencode(params)))
    return url


@none_safe
@log
def get(endpoint: str,
        encoding: str="utf-8",
        return_none_safe: bool=USE_NONE_SAFE_VALUES,
        **params) -> (list, dict, None):
    """
        Return requested data in JSON

        Check request has correct schema.

        :param endpoint - endpoint for request.
        :param encoding - encoding for received data.
        :param return_none_safe - return empty list on fallback.
        :param params - requested params
    """
    if not is_valid_schema(endpoint, **params):
        return [] if return_none_safe else None

    url = make_url(endpoint, **params)
    try:
        response = request.urlopen(url)
        return json.loads(response.read().decode(encoding))
    except (error.HTTPError, error.URLError) as err:
        logging.debug("Can't get '%s'.\n%s", url, err)
    return [] if return_none_safe else None
