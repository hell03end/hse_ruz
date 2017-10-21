import json
import re
from collections import Iterable
from datetime import datetime as dt
from datetime import timedelta as td
from functools import lru_cache
from http.client import HTTPResponse
from urllib import error, parse, request

from ruz.utils import (EMAIL_DOMAINS, EMAIL_PATTERN, REQUEST_SCHEMA,
                       RUZ_API_ENDPOINTS, RUZ_API_URL, Logger)


class RUZ(object):
    '''
        Handler for RUZ API

        All methods are transformed from CamelCase to _ notation.
    '''

    def __init__(self, strict_v1: bool=True, **kwargs):
        '''
            >>> RUZ(base_url=None)
            Traceback (most recent call last):
                ...
            PermissionError: Can't get base url!
            >>> RUZ(strict_v1=False)._url2[-2]
            '2'
            >>> RUZ()._url2 == RUZ()._url
            True
        '''
        self._url = kwargs.pop('base_url', RUZ_API_URL)
        if not self._url:
            raise PermissionError("Can't get base url!")
        self._endpoints = kwargs.pop('endpoints', RUZ_API_ENDPOINTS)
        self._url2 = self._url
        self._schema = kwargs.pop('schema', REQUEST_SCHEMA)
        self._logger = Logger(str(self.__class__))
        if not strict_v1:
            self._url2 += r"v2/"
        super(RUZ, self).__init__()

    @property
    def schema(self) -> dict:
        ''' Current request schema. '''
        return self._schema

    @property
    def v(self) -> int:
        '''
            Max API version

            >>> RUZ().v
            1
            >>> RUZ(strict_v1=False).v
            2
        '''
        return 2 if self._url2[-2] == "2" else 1

    @property
    def email_domains(self) -> tuple:
        ''' Allowed email domains '''
        return EMAIL_DOMAINS

    def _make_url(self, endpoint: str, data: dict=None, v: int=1) -> str:
        ''' Creates full url for API requests '''
        url = self._url if v == 1 or self.v == 1 else self._url2
        if data:
            return "{}{}?{}".format(url, self._endpoints[endpoint],
                                    parse.urlencode(data))
        return "{}{}".format(url, self._endpoints[endpoint])

    def _request(self, endpoint: str, data: dict=None) -> HTTPResponse:
        ''' Implements request to API with given params '''
        if self.v == 2:
            try:
                return request.urlopen(self._make_url(endpoint, data, v=2))
            except error.HTTPError as excinfo:
                self._logger.warning("v2 API unavailable: %s", excinfo)
        return request.urlopen(self._make_url(endpoint, data))

    def _verify_schema(self, endpoint: str, **params) -> None:
        '''
            Check params fit schema for certain endpoint

            >>> RUZ()._verify_schema("")
            Traceback (most recent call last):
                ...
            ValueError: Wrong endpoint: ''
        '''
        schema = self._schema.get(endpoint)
        if schema is None:
            raise KeyError("Wrong endpoint: '{}'".format(endpoint))
        for key, value in params.items():
            if key not in schema:
                raise KeyError("Wrong param '{}' for {} endpoint".format(
                    key, endpoint
                ))
            if not isinstance(value, schema[key]):
                raise ValueError("Expected {} for {} got: {}".format(
                    schema[key], key, type(value)
                ))

    def check_email(self, email: str, pattern: str=EMAIL_PATTERN) -> None:
        '''
            Check email is valid HSE corp. email.

            >>> RUZ().check_email("somemail@hse.com")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email address: somemail@hse.com
            >>> not RUZ().check_email("somemail@edu.hse.ru")
            True
            >>> RUZ().check_email("somem@il@edu.hse.ru")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email address: somem@il@edu.hse.ru
            >>> RUZ().check_email("somemail@google.ru")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email domain: google.ru
        '''
        if not re.match(pattern, email):
            raise ValueError("Wrong email address: {}".format(email))

        domain = email.split('@')[-1]
        if domain not in self.email_domains:
            raise ValueError("Wrong email domain: {}".format(domain))

    def _verify_email(self, email: str, receiver_type: int=3) -> None:
        '''
            Check email is valid for given receiver type (to use in API)

            >>> RUZ()._verify_email("somemail@hse.com")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email address: somemail@hse.com
            >>> not RUZ()._verify_email("somemail@edu.hse.ru")
            True
            >>> RUZ()._verify_email("somem@il@edu.hse.ru")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email address: somem@il@edu.hse.ru
            >>> RUZ()._verify_email("somemail@google.ru")
            Traceback (most recent call last):
                ...
            ValueError: Wrong email domain: google.ru
            >>> RUZ()._verify_email("somemail@hse.ru", -1)
            Traceback (most recent call last):
                ...
            ValueError: Wrong receiverType: -1
            >>> RUZ()._verify_email("somemail@hse.ru", 2)
            Traceback (most recent call last):
                ...
            ValueError: No email needed for receiverType: 2
        '''
        self.check_email(email)

        domain = email.split('@')[-1]
        if receiver_type == 1:
            if domain != "hse.ru":
                self._logger.warning("Wrong domain for teacher: %s", domain)
        elif receiver_type == 2:
            raise ValueError("No email needed for receiverType: 2")
        elif receiver_type == 3:
            if domain != "edu.hse.ru":
                self._logger.warning("Wrong domain for student: %s", domain)
        else:
            raise ValueError("Wrong receiverType: {}".format(receiver_type))

    def _get(self, endpoint: str, **params) -> dict:
        ''' Return requested data in JSON '''
        email = params.get('email')
        if email:
            self._verify_email(email, params.get('receiverType', 3))
        self._verify_schema(endpoint, **params)
        try:
            response = self._request(endpoint, data=params)
            return json.loads(response.read().decode('utf-8'))
        except error.HTTPError as excinfo:
            self._logger.error(excinfo)
            return {}

    def schedule(self, email: str=None,
                 from_date: str=str(dt.now()).replace('-', '.')[:10],
                 to_date: str=str(dt.now() + td(days=6)).replace('-',
                                                                 '.')[:10],
                 **params) -> dict:
        '''
            Return classes schedule.

            :param from_date: str, required. Start of the period YYYY.MM.DD.
            :param to_date: str, required. End of the period YYYY.MM.DD.
            :param receiverType: int. Type of the schedule
                (1/2/3 for teacher/auditorium/student).
            :param groupOid: int. ID of group.
            :param lecturerOid: int. ID of teacher.
            :param auditoriumOid: int. ID of auditorium.
            :param studentOid: int. ID of student.
            :param email: str. Email on hse.ru (edu.hse.ru for students).

            One of the followed required: lecturerOid, groupOid, auditoriumOid,
                studentOid, email.
        '''
        return self._get(
            "schedule",
            fromDate=params.pop('fromDate', from_date),
            toDate=params.pop('toDate', to_date),
            email=email,
            **params
        )

    def schedules(self, emails: Iterable, **params) -> map:
        '''
            Classes schedule for multiply students

            >>> RUZ().schedules(123)
            Traceback (most recent call last):
                ...
            ValueError: Expect Iterable, got: <class 'int'>
        '''
        if isinstance(emails, str):
            emails = [emails]
        elif not isinstance(emails, (set, list, tuple)):
            raise ValueError("Expect Iterable, got: {}".format(type(emails)))
        return map(lambda email, params=params: self.schedule(email, **params),
                   emails)

    @lru_cache(maxsize=16)
    def groups(self, **params) -> dict:
        '''
            Return list of groups.

            :param facultyOid: int. Course ID.
            :param findText: str. Text to find.
        '''
        return self._get("groups", **params)

    @lru_cache(maxsize=16)
    def staff_of_group(self, group_id: int, **params) -> dict:
        '''
            Return list of students in group.

            :param group_id: int, required. Group' ID.
            :param findText: str. Text to find.
        '''
        return self._get("staffOfGroup", groupOid=group_id, **params)

    @lru_cache(maxsize=16)
    def streams(self, **params) -> dict:
        '''
            Return list of study streams.

            :param findText: str. Text to find.
        '''
        return self._get("streams", **params)

    @lru_cache(maxsize=16)
    def staff_of_streams(self, stream_id: int, **params) -> dict:
        '''
            Return list of the groups on study stream.

            :param stream_id: int, required. Group' ID.
        '''
        return self._get("staffOfStreams", streamOid=stream_id, **params)

    @lru_cache(maxsize=16)
    def lecturers(self, **params) -> dict:
        '''
            Return list of teachers.

            :param chairOid: int. ID of department.
            :param findText: str. Text to find.
        '''
        return self._get("lecturers", **params)

    @lru_cache(maxsize=16)
    def auditoriums(self, **params) -> dict:
        '''
            Return list of auditoriums.

            :param buildingOid: int. ID of building.
            :param findText: str. Text to find.
        '''
        return self._get("auditoriums", **params)

    @lru_cache(maxsize=1)
    def type_of_auditoriums(self) -> dict:
        ''' Return list of auditoriums' types. '''
        return self._get("typeOfAuditoriums")

    @lru_cache(maxsize=1)
    def kind_of_works(self) -> dict:
        ''' Return list of classes' types. '''
        return self._get("kindOfWorks")

    @lru_cache(maxsize=16)
    def buildings(self, **params) -> dict:
        '''
            Return list of buildings.

            :param findText: str. Text to find.
        '''
        return self._get("buildings", **params)

    @lru_cache(maxsize=16)
    def faculties(self, **params) -> dict:
        '''
            Return list of learning programs (faculties).

            :param findText: str. Text to find.
        '''
        return self._get("faculties", **params)

    @lru_cache(maxsize=16)
    def chairs(self, **params) -> dict:
        '''
            Return list of departments.

            :param facultyOid: int. ID of course (learning program).
            :param findText: str. Text to find.
        '''
        return self._get("chairs", **params)

    @lru_cache(maxsize=16)
    def sub_groups(self, **params) -> dict:
        '''
            Return list of subgroups.

            :param findText: str. Text to find.
        '''
        return self._get("subGroups", **params)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
