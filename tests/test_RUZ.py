""" Minimal tests for ruz functionality """

import re
from datetime import datetime, timedelta

import pytest

import ruz
from ruz.schema import API_ENDPOINTS
from ruz.utils import API_URL
from tests import logging
from tests.fixtures import (NON_TRUSTED_EMAILS, SAMPLE_SCHEDULE,
                            SPLITED_SCHEDULE, TRUSTED_EMAILS,
                            TRUSTED_LECTURER_ID)


def test_is_student():
    assert not ruz.utils.is_student(TRUSTED_EMAILS['lecturer'])
    assert ruz.utils.is_student(TRUSTED_EMAILS['student'])
    assert ruz.utils.is_student(NON_TRUSTED_EMAILS['other']) is None


def test_is_hse_email():
    for email in ("somemail@hse.com", "somem@il@edu.hse.ru",
                  "somemail@google.ru", NON_TRUSTED_EMAILS['other']):
        assert not ruz.utils.is_hse_email(email)
    for email in (NON_TRUSTED_EMAILS['hse'], TRUSTED_EMAILS['student'],
                  TRUSTED_EMAILS['lecturer']):
        assert ruz.utils.is_hse_email(email)


# minimal functionality test
def test_is_valid_hse_email():
    for email in TRUSTED_EMAILS.values():
        assert ruz.utils.is_valid_hse_email(email)
    for email in NON_TRUSTED_EMAILS.values():
        assert not ruz.utils.is_valid_hse_email(email)


def test_get_formated_date():
    with pytest.raises(ValueError):
        ruz.utils.get_formated_date("x")

    for bias in (1, 1.1, 1., "1", "1.1", -1, 0, "-1", -1, "-1.", "01."):
        ruz_date = ruz.utils.get_formated_date(bias)
        assert ruz_date
        assert isinstance(ruz_date, str)
        assert len(ruz_date) == 10
        assert re.match(r"[\d]{4}(\.)[\d]{2}\1[\d]{2}", ruz_date)

    assert ruz.utils.get_formated_date(0) > ruz.utils.get_formated_date(-1)
    assert ruz.utils.get_formated_date(0) < ruz.utils.get_formated_date(1)
    assert ruz.utils.get_formated_date(0) == \
        ruz.utils.get_formated_date(0.000001)

    yesterday = datetime.now() - timedelta(days=float(1))
    assert ruz.utils.get_formated_date() == \
        ruz.utils.get_formated_date(date=datetime.now())
    assert ruz.utils.get_formated_date(-1) == \
        ruz.utils.get_formated_date(date=yesterday)


def test_make_url():
    with pytest.raises(KeyError):
        ruz.utils.make_url("")
    for key, endpoint in API_ENDPOINTS.items():
        assert ruz.utils.make_url(key) == API_URL + endpoint
        assert ruz.utils.make_url(key, v=1) == "?".join((
            API_URL + endpoint, "v=1"
        ))


# tests not all cases (type of param, etc.)
def test_is_valid_schema():
    assert not ruz.utils.is_valid_schema("")
    for endpoint in API_ENDPOINTS.keys():
        if endpoint == 'schedule':
            assert not ruz.utils.is_valid_schema(
                endpoint, email=NON_TRUSTED_EMAILS['other']
            )
            assert not ruz.utils.is_valid_schema(endpoint)
            for email in TRUSTED_EMAILS.values():
                assert ruz.utils.is_valid_schema(endpoint, email=email,
                                                 check_email_online=False)
        else:
            assert not ruz.utils.is_valid_schema(endpoint, tmp=None)
            assert ruz.utils.is_valid_schema(endpoint)


# tests only negative cases, positive cases are tested in test_schema
def test_get():
    for endpoint in API_ENDPOINTS.keys():
        if endpoint == "schedule":
            response = ruz.utils.get(
                endpoint,
                email=NON_TRUSTED_EMAILS['other'],
                return_none_safe=True,
                check_email_online=False
            )
        else:
            response = ruz.utils.get(endpoint, tmp=123, return_none_safe=True)
        assert not response
        assert isinstance(response, list)


def test_schedules():
    with pytest.raises(ValueError) as excinfo:
        ruz.schedules()
    assert excinfo

    for schedule in ruz.schedules(emails=TRUSTED_EMAILS.values(),
                                  return_none_safe=False):
        assert schedule is not None

    schedule_map = ruz.schedules(lecturer_ids=[TRUSTED_LECTURER_ID],
                                 return_none_safe=False)
    assert isinstance(schedule_map, map)


def test_find_by_str():
    with pytest.raises(KeyError):
        ruz.find_by_str("tmp", "some query")
    with pytest.raises(NotImplementedError):
        ruz.find_by_str(min, "some query")


def test_split_schedule_by_days():
    days_split = ruz.utils.split_schedule_by_days(SAMPLE_SCHEDULE)
    assert SPLITED_SCHEDULE == days_split
