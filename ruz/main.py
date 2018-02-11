import json
import re
from collections import Callable, Iterable
from datetime import datetime, timedelta
from functools import lru_cache
from urllib import error, parse, request

from ruz.logging import log, logging
from ruz.schema import REQUEST_SCHEMA, RUZ_API_ENDPOINTS
from ruz.utils import (CHECK_EMAIL_ONLINE, RUZ_API_URL, RUZ_API_V,
                       USE_NONE_SAFE_VALUES, none_safe)


# ===== Common methods =====

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

    logging.error("Wrong HSE email domain: '%s'", email_domain)


def is_hse_email(email: str) -> bool:
    """
        Check email is valid HSE corp. email

        :param email, required - email address to check.
    """
    if re.fullmatch(r"^[a-z0-9\._-]{3,}@(edu\.)?hse\.ru$", email.lower()):
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


@log()
def is_valid_hse_email(email: str) -> bool:
    """
        Check email is valid via API endpoint call (schedule)

        :param email - email address to check (for schedules only).
    """
    @none_safe()
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


# ===== Special methods =====

@log()
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
            logging.warning("'%s' is not verified by API call.", email)
        del email

    endpoint = RUZ_API_ENDPOINTS.get(endpoint)
    if endpoint is None:
        logging.warning("Can't find endpoint: '%s'.", endpoint)
        del endpoint
        return False

    schema = REQUEST_SCHEMA[endpoint]
    for key, value in params.items():
        if key not in schema:
            logging.warning("Can't find '%s' schema param: '%s'",
                            endpoint, key)
            del schema, endpoint
            return False
        if not isinstance(value, schema[key]):
            logging.warning("Expected {} for '{}'::'{}' got: {}",
                            schema[key], endpoint, key, type(value))
            del schema, endpoint
            return False
    del schema, endpoint
    return True


@log()
def make_url(endpoint: str, **params) -> str:
    """
        Creates URL for API requests

        :param endpoint - endpoint for request.
        :param params - request params.
    """
    url = "".join((RUZ_API_URL, RUZ_API_ENDPOINTS[endpoint]))
    if params:
        return "?".join((url, parse.urlencode(params)))
    return url


@none_safe()
@log()
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
        logging.warning("Can't get '%s'.\n%s", url, err)
    return [] if return_none_safe else None


# ===== API methods =====

def schedules(emails: Iterable=None,
              lecturer_ids: Iterable=None,
              auditorium_ids: Iterable=None,
              student_ids: Iterable=None,
              **params) -> map:
    """
        Classes schedule for multiply students/lecturers as generator

        See RUZ::person_lessons for more details.
        One of the followed required: lecturer_ids, auditorium_ids,
            student_ids, emails. Throw an exception.

        :param emails - emails on hse.ru (edu.hse.ru for students).
        :param lecturer_ids - IDs of teacher.
        :param auditorium_ids - IDs of auditorium.
        :param student_ids - IDs of student.
    """
    def get_handler(key: str) -> Callable:
        def func(val: dict) -> list or dict:
            return person_lessons(**{key: val}, **params)
        return func

    if emails:
        return map(get_handler("email"), emails)
    elif lecturer_ids:
        return map(get_handler("lecturer_id"), lecturer_ids)
    elif auditorium_ids:
        return map(get_handler("auditorium_id"), auditorium_ids)
    elif student_ids:
        return map(get_handler("student_id"), student_ids)

    raise ValueError("One of the followed required: lecturer_ids, "
                     "auditorium_ids, student_ids, emails")


def person_lessons(email: str=None,
                   from_date: str=get_formated_date(),
                   to_date: str=get_formated_date(6),  # one week
                   receiver_type: int=None,
                   lecturer_id: int=None,
                   auditorium_id: int=None,
                   student_id: int=None,
                   **params) -> list:
    """
        Return classes schedule (for week by default)

        Automatically choose receiver type from given email address.
        There is no need to specify receiver type for students explicitly.
        One of the followed required: lecturer_id, auditorium_id,
            student_id, email. Throws an exception.
        Default values (fromDate, toDate) are set to return schedule for
            one week from now.

        :param email - email on hse.ru (edu.hse.ru for students).
        :param from_date, required - start of the period YYYY.MM.DD.
        :param to_date, required - end of the period YYYY.MM.DD.
        :param receiver_type - type of the schedule
            (1/2/3 for teacher/auditorium/student).
        :param lecturer_id - ID of teacher.
        :param auditorium_id - ID of auditorium.
        :param student_id - ID of student.
        :param check_online :type bool - online verification for email.
        :param safe :type bool - return something even if no data received.
    """
    if receiver_type is None:
        if email is not None and not is_student(email):
            logging.debug("Detect lecturer email: '%s'.", email)
            receiver_type = 1
        elif lecturer_id is not None:
            logging.debug("Detect lecturer %d.", lecturer_id)
            receiver_type = 1
        elif auditorium_id is not None:
            logging.debug("Detect auditorium %d.", auditorium_id)
            receiver_type = 2
    elif receiver_type == 3:
        receiver_type = None

    return get(
        "schedule",
        fromDate=from_date,
        toDate=to_date,
        email=email,
        receiverType=receiver_type,
        lecturerOid=lecturer_id,
        auditoriumOid=auditorium_id,
        studentOid=student_id,
        **params
    )


def groups(faculty_id: int=None) -> list:
    """
        Return collection of groups

        :param faculty_id - course ID.
    """
    return get("groups", facultyOid=faculty_id)


def staff_of_group(group_id: int) -> list:
    """
        Return collection of students in group

        :param group_id, required - group' ID.
    """
    return get("staffOfGroup", groupOid=group_id)


@lru_cache(maxsize=1)
def streams(reset_cache: bool=False) -> list:
    """
        Return collection of study streams

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("streams")


def lecturers(chair_id: int=None) -> list:
    """
        Return collection of teachers

        :param chair_id - ID of department.
    """
    return get("lecturers", chairOid=chair_id)


def auditoriums(building_id: int=None) -> list:
    """
        Return collection of auditoriums

        :param building_id - ID of building.
    """
    return get("auditoriums", buildingOid=building_id)


@lru_cache(maxsize=1)
def type_of_auditoriums(reset_cache: bool=False) -> list:
    """
        Return collection of auditoriums' types

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("typeOfAuditoriums")


@lru_cache(maxsize=1)
def kind_of_works(reset_cache: bool=False) -> list:
    """
        Return collection of classes' types

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("kindOfWorks")


@lru_cache(maxsize=1)
def buildings(reset_cache: bool=False) -> list:
    """
        Return collection of buildings

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("buildings")


@lru_cache(maxsize=1)
def faculties(reset_cache: bool=False) -> list:
    """
        Return collection of learning programs

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("faculties")


def chairs(faculty_id: int=None) -> list:
    """
        Return collection of departments

        :param faculty_id - ID of course (learning program).
    """
    return get("chairs", facultyOid=faculty_id)


@lru_cache(maxsize=1)
def sub_groups(reset_cache: bool=False) -> list:
    """
        Return collection of subgroups

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("subGroups")


# ===== Additional methods =====

def find_by_str(subject: str or Callable,
                query: str,
                by: str="name",
                **params) -> list:
    """
        Linear search for subject by given text field (as query)

        Search method is very straightforward. For more complex searches
        use custom implementation.
        Throws an exception:
            * KeyError if no subject found.
            * NotImplementedError if method is not implemented for subject.

        :param subject - subject to find: possible variants:
            * buildings: 'name', 'address', 'abbr';
            * faculties: 'name', 'institute', 'abbr';
            * sub_groups: 'name', 'group', 'abbr';
            * streams: 'name', 'faculty', 'abbr', 'formOfEducation', 'course';
            * type_of_auditoriums: 'name', 'abbr';
            * kind_of_works: 'name', 'abbr';
            * chairs: 'name', 'faculty', 'abbr';
            * auditoriums: 'number', 'building', 'typeOfAuditorium';
            * lecturers: 'chair', 'fio', 'shortFIO';
            * groups: 'faculty', 'formOfEducation', 'number', 'speciality';
            * staff_of_group: 'fio', 'shortFIO';
            * person_lessons: 'building', 'date', 'beginLesson', 'auditorium',
                'dateOfNest', 'dayOfWeekString', 'detailInfo', 'discipline',
                'disciplineinplan', 'endLesson', 'kindOfWork', 'lecturer',
                'stream'.
        :param query - text query to find.
        :param by - search field.
    """
    SUBJECTS = {
        buildings.__name__: buildings,
        faculties.__name__: faculties,
        sub_groups.__name__: sub_groups,
        streams.__name__: streams,
        type_of_auditoriums.__name__: type_of_auditoriums,
        kind_of_works.__name__: kind_of_works,
        chairs.__name__: chairs,
        auditoriums.__name__: auditoriums,
        lecturers.__name__: lecturers,
        groups.__name__: groups,
        staff_of_group.__name__: staff_of_group,
        person_lessons.__name__: person_lessons
    }

    if not isinstance(subject, Callable):
        subject = SUBJECTS[subject]
    elif subject.__name__ not in SUBJECTS.keys():
        raise NotImplementedError(subject.__name__)

    query = query.strip().lower()
    return [el for el in subject(**params) if query in el[by].lower().strip()]
