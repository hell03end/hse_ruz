import json
import re
from collections import Iterable
from copy import deepcopy
from datetime import datetime as dt
from datetime import timedelta as td
from functools import lru_cache
from http.client import HTTPResponse
from urllib import error, parse, request

from ruz.utils import (EMAIL_DOMAINS, EMAIL_PATTERN, REQUEST_SCHEMA,
                       RUZ_API2_ENDPOINTS, RUZ_API2_URL, RUZ_API_ENDPOINTS,
                       RUZ_API_URL, Logger, log, none_safe)


class RUZ(object):
    """
        Handler for RUZ API

        Both CamelCase and snake_notation supported for method names and
        params. CamelCase is depreciated.

        Usage
        -----
        >>> api = RUZ()
    """

    def __init__(self, strict_v1: bool=False, **kwargs):
        """
            :param strict_v1 - force usage of api v1.

            Advanced
            --------
            :param base_url :type str - valid entry point to HSE RUZ API.
            :param endpoints :type dict - endpoints for API.
            :param schema :type dict - schema for request params of each
                endpoint (to validate params).
            :param domains :type Iterable - collection of valid HSE domains.

            Usage
            -----
            >>> RUZ(base_url=None)
            Traceback (most recent call last):
                ...
            PermissionError: Can't get base url!
            >>> RUZ(strict_v1=False)._url2[-2]
            '2'
            >>> RUZ()._url2 == RUZ()._url
            True
        """
        self._url = kwargs.pop('base_url', RUZ_API_URL)
        if not self._url or not isinstance(self._url, str):
            raise PermissionError("Can't get base url!")
        self._endpoints = kwargs.pop('endpoints', RUZ_API_ENDPOINTS)
        if not self._endpoints or not isinstance(self._endpoints, dict):
            raise ValueError("Can't find correct endpoints!")
        self._schema = kwargs.pop('schema', REQUEST_SCHEMA)
        if not isinstance(self._schema, (dict, list)):
            raise ValueError(
                "Expect list or dict, got: {}".format(type(self._schema))
            )
        self._domains = kwargs.pop('domains', EMAIL_DOMAINS)
        if not isinstance(self._domains, tuple):
            raise ValueError(
                "Expect domains as tuple, got: {}".format(type(self._domains))
            )
        self._logger = Logger(str(self.__class__))
        self._url2 = self._url
        self._endpoints2 = self._endpoints
        self._v = 1
        if not strict_v1:
            self._url2 = kwargs.pop('base_url', RUZ_API2_URL)
            self._endpoints2 = kwargs.pop('endpoints', RUZ_API2_ENDPOINTS)
            self._v = 2
        super(RUZ, self).__init__()

    @property
    def ok(self) -> bool:
        """
            Check internet connection is ok by connecting to google servers

            Usage
            -----
            >>> RUZ().ok
            True
        """
        try:
            r = request.urlopen(r"http://google.com")
            del r
        except error.URLError as err:
            self._logger.info("Can't connect to google.com: %s", err)
            return False
        return True

    @property
    def schema(self) -> dict:
        """
            (copy of) Current request schema

            Usage
            -----
            >>> RUZ().schema is not RUZ().schema
            True
        """
        return deepcopy(self._schema)

    @property
    def v(self) -> int:
        """
            Max API version

            Usage
            -----
            >>> RUZ(strict_v1=True).v
            1
            >>> RUZ(strict_v1=False).v
            2
        """
        return self._v

    @property
    def domains(self) -> tuple:
        """
            Collection of valid HSE email domains

            Usage
            -----
            >>> isinstance(RUZ().domains, tuple)
            True
        """
        return self._domains

    @property
    def endpoints(self) -> dict:
        """
            Collection HSE API endpoints

            Usage
            -----
            >>> isinstance(RUZ().endpoints, dict)
            True
            >>> RUZ().endpoints is not RUZ().endpoints
            True
        """
        return deepcopy(self._endpoints)

    @property
    def endpoints2(self) -> dict:
        """
            Collection HSE API endpoints for API v2

            Usage
            -----
            >>> isinstance(RUZ().endpoints2, dict)
            True
            >>> RUZ().endpoints2 is not RUZ().endpoints2
            True
        """
        return deepcopy(self._endpoints2)

    @staticmethod
    def is_student(email: str) -> bool:
        """
            Check user is student or not by HSE email address

            :param email, required - valid HSE email addres or domain.

            Usage
            -----
            >>> RUZ.is_student("somemail@hse.ru")
            False
            >>> RUZ.is_student("somemail@edu.hse.ru")
            True
        """
        if not isinstance(email, str):
            raise ValueError("Expect str, got: {}".format(type(email)))
        domain = email
        if r"@" in email:
            domain = email.split(r'@')[-1]
        if domain == "edu.hse.ru":
            return True
        elif domain == "hse.ru":
            return False
        raise ValueError("Wrong HSE domain: {}".format(domain))

    @log
    def _make_url(self, endpoint: str, data: dict=None, v: int=1) -> str:
        """
            Creates full url for API requests

            :param endpoint - endpoint for request.
            :param data - request params.
            :param v - API version to use (v1 is always used as fallback).

            Usage
            -----
            >>> RUZ()._make_url("schedule")
            http://92.242.58.221/ruzservice.svc/personLessons
            >>> RUZ()._make_url("schedule", data={'email': 123})
            http://92.242.58.221/ruzservice.svc/personLessons?email=123
        """
        url = self._url
        endpoint = self._endpoints[endpoint]
        if v != 1 and self.v != 1:
            url = self._url2
            endpoint = self._endpoints2[endpoint]
        if data:
            return "{}{}?{}".format(url, endpoint, parse.urlencode(data))
        return "{}{}".format(url, endpoint)

    @log
    def _request(self, endpoint: str, data: dict=None) -> HTTPResponse:
        """
            Implements request to API with given params

            :param endpoint - endpoint for request.
            :param data - request params.

            Usage
            -----
            >>> RUZ()._request("schedule", data={'email': "user@hse.ru"})
            Traceback (most recent call last):
                ...
            urllib.error.HTTPError: HTTP Error 400: Bad Request
        """
        if self._v == 2:
            # api v2 may be unreachable for some API methods
            try:
                return request.urlopen(self._make_url(endpoint, data, v=2))
            except (error.HTTPError, error.URLError) as excinfo:
                self._logger.warning("v2 API unreachable for '%s': %s",
                                     endpoint, excinfo)
        return request.urlopen(self._make_url(endpoint, data))

    @log
    def _verify_schema(self, endpoint: str, **params) -> None:
        """
            Check params fit schema for certain endpoint

            :param endpoint - endpoint for request.
            :param check_online :type bool - check email throw API call.
            schema params passes with **params.

            Usage
            -----
            >>> RUZ()._verify_schema("")
            Traceback (most recent call last):
                ...
            ValueError: Wrong endpoint: ''
        """
        if (endpoint == "schedule" and "lecturerOid" not in params and
                "studentOid" not in params and "email" not in params and
                "auditoriumOid" not in params):
            raise ValueError("One of the followed required: lecturer_id, "
                             "auditorium_id, student_id, email for "
                             "schedule endpoint.")
        email = params.get('email')
        if email:
            self.verify_email(
                email,
                params.get('receiverType', 3),
                params.pop('check_online', False)
            )
        endpoint = self._endpoints[endpoint]  # it's ok to use only v1 here
        schema = self._schema.get(endpoint)
        if schema is None:
            raise KeyError("Wrong endpoint: '{}'".format(endpoint))
        for key, value in params.items():
            if key not in schema:
                raise KeyError("Wrong param '{}' for '{}' endpoint".format(
                    key, endpoint
                ))
            if not isinstance(value, schema[key]):
                raise ValueError("Expected {} for '{}'::'{}' got: {}".format(
                    schema[key], endpoint, key, type(value)
                ))

    @staticmethod
    def check_email(email: str, pattern: str=EMAIL_PATTERN) -> None:
        """
            Check email is valid HSE corp. email

            Throws an exception

            :param email, required - email address to check.
            :param pattern - pattern to check against.

            Usage
            -----
            >>> RUZ.check_email("somemail@hse.com")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email address: somemail@hse.com
            >>> not RUZ.check_email("somemail@edu.hse.ru")
            True
            >>> RUZ.check_email("somem@il@edu.hse.ru")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email address: somem@il@edu.hse.ru
            >>> RUZ.check_email("somemail@google.ru")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email domain: google.ru
        """
        if not isinstance(email, str):
            raise ValueError("Expect str, got: {}".format(type(email)))
        elif not re.match(pattern, email):
            raise ValueError("Wrong email address: {}".format(email))

        domain = email.split('@')[-1]
        if domain not in EMAIL_DOMAINS:
            raise ValueError("Wrong email domain: {}".format(domain))
        del domain

    @staticmethod
    def date(day_bias: int=0) -> str:
        """
            Return date in RUZ API compatible format

            :param day_bias - number of day from now.

            Usage
            -----
            >>> isinstance(RUZ.date(), str)
            True
            >>> RUZ.date('abc')
            Traceback (most recent call last):
                ...
            ValueError: Expect int, got: <class 'int'>
        """
        if not isinstance(day_bias, int):
            raise ValueError("Expect int, got: {}".format(type(day_bias)))
        if day_bias < 0:
            return (dt.now() - td(days=-day_bias)).strftime(r'%Y.%m.%d')
        return (dt.now() + td(days=day_bias)).strftime(r'%Y.%m.%d')

    @lru_cache(maxsize=128)
    @log
    def verify_email(self, email: str, receiver_type: int=3,
                     check_online: bool=False) -> None:
        """
            Check email is valid for given receiver type (to use in API)

            Throw an exception.

            :param email - email address to check (for schedules only).
            :param receiver_type - type of requested schedule if any.
            :param check_online - check email throw API call.

            Usage
            -----
            >>> RUZ().verify_email("somemail@hse.com")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email address: somemail@hse.com
            >>> not RUZ().verify_email("somemail@edu.hse.ru")
            True
            >>> RUZ().verify_email("somem@il@edu.hse.ru")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email address: somem@il@edu.hse.ru
            >>> RUZ().verify_email("somemail@google.ru")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email domain: google.ru
            >>> RUZ().verify_email("somemail@hse.ru", -1)
            Traceback (most recent call last):
                ...
            ValueError: Wrong receiverType: -1
            >>> RUZ().verify_email("somemail@hse.ru", 2)
            Traceback (most recent call last):
                ...
            ValueError: No email needed for receiverType: 2
        """
        RUZ.check_email(email)

        domain = email.split('@')[-1]
        if receiver_type == 1:
            if domain != "hse.ru":
                self._logger.warning("Wrong domain for teacher: %s", domain)
        elif receiver_type == 2:
            del domain
            raise ValueError("No email needed for receiverType: 2")
        elif receiver_type == 3:
            if domain != "edu.hse.ru":
                self._logger.warning("Wrong domain for student: %s", domain)
        else:
            del domain
            raise ValueError("Wrong receiverType: {}".format(receiver_type))

        if check_online:
            try:
                response = self._request(
                    "schedule",
                    data={
                        'email': email,
                        'fromDate': RUZ.date(),
                        'toData': RUZ.date(1)
                    }
                )
                del response
            except (error.HTTPError, error.URLError) as excinfo:
                self._logger.debug(excinfo)
                raise ValueError(
                    "(online) Wrong HSE email address: {}".format(email)
                )

    @none_safe
    @log
    def _get(self, endpoint: str, encoding: str="utf-8", safe: bool=True,
             **params) -> (list, None):
        """
            Return requested data in JSON

            Check request has correct schema. Throw an exception.

            :param endpoint - endpoint for request.
            :param encoding - encoding for received data.
            :param safe - return empty list even if no data received.
            Request params passes throw **params.

            Usage
            -----
            >>> isinstance(RUZ()._get("kindOfWorks"), list)
            True
        """
        self._verify_schema(endpoint, **params)
        try:
            response = self._request(endpoint, data=params)
            return json.loads(response.read().decode(encoding))
        except error.HTTPError as excinfo:
            self._logger.error(excinfo)
            if safe:
                return []
            return

    def _map_schedules(self, key: str, vals: Iterable,
                       allowed_types: tuple=(str,), **params) -> map:
        """
            Return map for fetching schedules with given vals

            Throw an exception.

            :param name - name of API param.
            :param vals - values to map with person_lessons.
            :param allowed_types - type(s) of values.

            Usage
            -----
            >>> isinstance(RUZ()._map_schedules("abc"), map)
            True
        """
        if not isinstance(key, str):
            raise ValueError("Expect str, got: {}".format(type(key)))
        if isinstance(vals, allowed_types):
            vals = (vals,)
        if not isinstance(vals, (tuple, set, list)):
            raise ValueError("Expect Iterable or {}, got: {}".format(
                allowed_types, type(vals)))

        def func(val: dict, key: str=key, params: dict=params) -> list:
            params.update({key: val})
            return self.person_lessons(**params)
        return map(func, vals)

    def schedules(self,
                  emails: Iterable=None,
                  lecturer_ids: Iterable=None,
                  auditorium_ids: Iterable=None,
                  student_ids: Iterable=None,
                  **params) -> map:
        """
            Classes schedule for multiply students/lecturers as generator

            See RUZ::person_lessons for more details.
            Throw an exception.

            :param emails - emails on hse.ru (edu.hse.ru for students).
            :param lecturer_ids - IDs of teacher.
            :param auditorium_ids - IDs of auditorium.
            :param student_ids - IDs of student.

            One of the followed required: lecturer_ids, auditorium_ids,
                student_ids, emails.

            Usage
            -----
            >>> RUZ().schedules(emails=123)
            Traceback (most recent call last):
                ...
            ValueError: Expect Iterable or (<class 'str'>,), got: <class 'int'>
            >>> RUZ().schedules(lecturer_ids='abc')
            Traceback (most recent call last):
                ...
            ValueError: Expect Iterable or (<class 'int'>,), got: <class 'str'>
        """
        # support CamelCase notation
        lecturer_ids = params.pop('lecturerOids', lecturer_ids)
        auditorium_ids = params.pop('auditoriumOids', auditorium_ids)
        student_ids = params.pop('studentOids', student_ids)
        if emails:
            return self._map_schedules("email", emails, **params)
        elif lecturer_ids:
            return self._map_schedules("lecturer_id", lecturer_ids, (int,),
                                       **params)
        elif auditorium_ids:
            return self._map_schedules("auditorium_id", auditorium_ids, (int,),
                                       **params)
        elif student_ids:
            return self._map_schedules("student_id", student_ids, (int,),
                                       **params)
        else:
            raise ValueError("One of the followed required: lecturer_ids, "
                             "auditorium_ids, student_ids, emails")

    def person_lessons(self,
                       email: str=None,
                       from_date: str=dt.now().strftime(r'%Y.%m.%d'),
                       to_date: str=(dt.now() +
                                     td(days=6)).strftime(r'%Y.%m.%d'),
                       receiver_type: int=None,
                       lecturer_id: int=None,
                       auditorium_id: int=None,
                       student_id: int=None,
                       **params) -> list:
        """
            Return classes schedule (for week by default)

            Automatically choose receiver type from given email address.
            If no email provided and auditorium_id is not None, automatically
            set receiver type for auditoriums.

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

            One of the followed required: lecturer_id, auditorium_id,
                student_id, email.

            Usage
            -----
            >>> assert RUZ().person_lessons("somemail@hse.ru")
        """
        if receiver_type is None and email is not None:
            if not RUZ.is_student(email):
                receiver_type = 1
        elif receiver_type is None and lecturer_id is not None:
            receiver_type = 1
        elif receiver_type is None and auditorium_id is not None:
            receiver_type = 2

        # no need to specify receiver type for students explicitly
        if receiver_type == 3:
            receiver_type = None

        return self._get(
            "schedule",
            fromDate=params.pop('fromDate', from_date),
            toDate=params.pop('toDate', to_date),
            email=email,
            receiverType=params.pop('receiverType', receiver_type),
            lecturerOid=params.pop('lecturerOid', lecturer_id),
            auditoriumOid=params.pop('auditoriumOid', auditorium_id),
            studentOid=params.pop('studentOid', student_id),
            **params
        )

    def groups(self, faculty_id: int=None, **params) -> list:
        """
            Return collection of groups

            :param faculty_id - course ID.

            Usage
            -----
            >>> assert RUZ().groups()
        """
        return self._get(
            "groups",
            facultyOid=params.pop('facultyOid', faculty_id)
        )

    def staff_of_group(self, group_id: int, **params) -> list:
        """
            Return collection of students in group

            :param group_id, required - group' ID.

            Usage
            -----
            >>> assert RUZ().staff_of_group(1)
        """
        return self._get(
            "staffOfGroup",
            groupOid=params.pop('groupOid', group_id)
        )

    def streams(self) -> list:
        """
            Return collection of study streams

            Cache requested values.

            Usage
            -----
            >>> assert RUZ().streams()
        """
        return self._get("streams")

    def staff_of_streams(self, stream_id: int, **params) -> list:
        """
            Return collection of the groups on study stream

            :param stream_id, required - group' ID.

            Usage
            -----
            >>> assert RUZ().staff_of_streams(45771)
        """
        return self._get(
            "staffOfStreams",
            streamOid=params.pop('streamOid', stream_id)
        )

    def lecturers(self, chair_id: int=None, **params) -> list:
        """
            Return collection of teachers

            :param chair_id - ID of department.

            Usage
            -----
            >>> assert RUZ().lecturers()
        """
        return self._get(
            "lecturers",
            chairOid=params.pop('chairOid', chair_id)
        )

    def auditoriums(self, building_id: int=None, **params) -> list:
        """
            Return collection of auditoriums

            :param building_id - ID of building.

            Usage
            -----
            >>> assert RUZ().auditoriums()
        """
        return self._get(
            "auditoriums",
            buildingOid=params.pop('buildingOid', building_id)
        )

    @lru_cache(maxsize=1)
    def type_of_auditoriums(self) -> list:
        """
            Return collection of auditoriums' types

            Cache requested values.

            Usage
            -----
            >>> assert RUZ().type_of_auditoriums()
        """
        return self._get("typeOfAuditoriums")

    @lru_cache(maxsize=1)
    def kind_of_works(self) -> list:
        """
            Return collection of classes' types

            Cache requested values.

            Usage
            -----
            >>> assert RUZ().kind_of_works()
        """
        return self._get("kindOfWorks")

    @lru_cache(maxsize=1)
    def buildings(self) -> list:
        """
            Return collection of buildings

            Cache requested values.

            Usage
            -----
            >>> assert RUZ().buildings()
        """
        return self._get("buildings")

    def faculties(self) -> list:
        """
            Return collection of learning programs (faculties)

            Usage
            -----
            >>> assert RUZ().faculties()
        """
        return self._get("faculties")

    def chairs(self, faculty_id: int=None, **params) -> list:
        """
            Return collection of departments

            :param faculty_id - ID of course (learning program).

            Usage
            -----
            >>> assert RUZ().chairs()
        """
        return self._get(
            "chairs",
            facultyOid=params.pop('facultyOid', faculty_id)
        )

    def sub_groups(self) -> list:
        """
            Return collection of subgroups

            Usage
            -----
            >>> assert RUZ().sub_groups()
        """
        return self._get("subGroups")

    def __bool__(self) -> bool:
        return self.ok

    # aliases
    def schedule(self, *args, **kwargs) -> list:
        """
            Alias for person_lessons method (backward compitability)

            (depreciated)
            Uses same args and kwargs as in person_lessons method.
            Look for more info in person_lessons help.

            Usage
            -----
            >>> assert RUZ().schedule("mysuperawesomeemail@hse.ru")
        """
        return self.person_lessons(*args, **kwargs)

    # for CamelCase compatibility
    def subGroups(self) -> list:
        return self.sub_groups()
    subGroups.__doc__ = sub_groups.__doc__

    def kindOfWorks(self) -> list:
        return self.kind_of_works()
    kindOfWorks.__doc__ = kind_of_works.__doc__

    def typeOfAuditoriums(self) -> list:
        return self.type_of_auditoriums()
    typeOfAuditoriums.__doc__ = type_of_auditoriums.__doc__

    def staffOfStreams(self, *args, **kwargs) -> list:
        return self.staff_of_streams(*args, **kwargs)
    staffOfStreams.__doc__ = staff_of_streams.__doc__

    def staffOfGroup(self, *args, **kwargs) -> list:
        return self.staff_of_group(*args, **kwargs)
    staffOfGroup.__doc__ = staff_of_group.__doc__

    def personLessons(self, *args, **kwargs) -> list:
        return self.person_lessons(*args, **kwargs)
    personLessons.__doc__ = person_lessons.__doc__


if __name__ == "__main__":
    import doctest
    doctest.testmod()
