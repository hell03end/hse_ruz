""" Minimal tests for ruz functionality """

import re

import pytest
from tests import (INTRUSTED_EMAILS, TRUSTED_EMAILS, TRUSTED_LECTURER_ID,
                   logging)

import ruz
from ruz.schema import RUZ_API_ENDPOINTS
from ruz.utils import RUZ_API_URL


# ===== Common methods =====

def test_is_student():
    assert not ruz.is_student(TRUSTED_EMAILS['lecturer'])
    assert ruz.is_student(TRUSTED_EMAILS['student'])
    assert ruz.is_student(INTRUSTED_EMAILS['other']) is None


def test_is_hse_email():
    for email in ("somemail@hse.com", "somem@il@edu.hse.ru",
                  "somemail@google.ru", INTRUSTED_EMAILS['other']):
        assert not ruz.is_hse_email(email)
    for email in (INTRUSTED_EMAILS['hse'], TRUSTED_EMAILS['student'],
                  TRUSTED_EMAILS['lecturer']):
        assert ruz.is_hse_email(email)


# minimal functionality test
def test_is_valid_hse_email():
    for email in TRUSTED_EMAILS.values():
        assert ruz.is_valid_hse_email(email)
    for email in INTRUSTED_EMAILS.values():
        assert not ruz.is_valid_hse_email(email)


def test_get_formated_date():
    with pytest.raises(ValueError):
        ruz.get_formated_date("x")

    for bias in (1, 1.1, 1., "1", "1.1", -1, 0, "-1", -1, "-1.", "01."):
        ruz_date = ruz.get_formated_date(bias)
        assert ruz_date
        assert isinstance(ruz_date, str)
        assert len(ruz_date) == 10
        assert re.match(r"[\d]{4}(\.)[\d]{2}\1[\d]{2}", ruz_date)

    assert ruz.get_formated_date(0) > ruz.get_formated_date(-1)
    assert ruz.get_formated_date(0) < ruz.get_formated_date(1)
    assert ruz.get_formated_date(0) == ruz.get_formated_date(0.000001)


# ===== Special methods =====

def test_make_url():
    with pytest.raises(KeyError):
        ruz.main.make_url("")
    for key, endpoint in RUZ_API_ENDPOINTS.items():
        assert ruz.main.make_url(key) == RUZ_API_URL + endpoint
        assert ruz.main.make_url(key, v=1) == "?".join((
            RUZ_API_URL + endpoint, "v=1"
        ))


# tests not all cases (type of param, etc.)
def test_is_valid_schema():
    assert not ruz.main.is_valid_schema("")
    for endpoint in RUZ_API_ENDPOINTS.keys():
        if endpoint == 'schedule':
            assert not ruz.main.is_valid_schema(
                endpoint, email=INTRUSTED_EMAILS['other']
            )
            assert not ruz.main.is_valid_schema(endpoint)
            for email in TRUSTED_EMAILS.values():
                assert ruz.main.is_valid_schema(endpoint, email=email,
                                                check_email_online=False)
        else:
            assert not ruz.main.is_valid_schema(endpoint, tmp=None)
            assert ruz.main.is_valid_schema(endpoint)


# tests only negative cases, positive cases are tested in test_schema
def test_get():
    for endpoint in RUZ_API_ENDPOINTS.keys():
        if endpoint == "schedule":
            none_safe = ruz.main.get(
                endpoint,
                email=INTRUSTED_EMAILS['other'],
                return_none_safe=True,
                check_email_online=False
            )
            usual = ruz.main.get(
                endpoint,
                email=INTRUSTED_EMAILS['other'],
                return_none_safe=False,
                check_email_online=False
            )
        else:
            none_safe = ruz.main.get(endpoint, tmp=123, return_none_safe=True)
            usual = ruz.main.get(endpoint, tmp=123, return_none_safe=False)
        assert not none_safe
        assert isinstance(none_safe, list)
        assert not usual
        assert usual is None


# ===== API methods =====

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
