import json
from functools import lru_cache
from http.client import HTTPResponse
from urllib import error, parse, request

from .utils import RUZ_API_ENDPOINTS, RUZ_API_URL, Logger


class RUZ(object):
    '''
        Handler for RUZ API

        All methods are transformed from CamelCase to _ notation.
    '''

    def __init__(self, strict_v1: bool=False, **kwargs):
        '''
            >>> RUZ(base_url=None)
            Traceback (most recent call last):
                ...
            PermissionError: Can't get base url!
            >>> RUZ()._url2[-2]
            '2'
            >>> RUZ(strict_v1=True)._url2 == RUZ()._url
            True
        '''
        self._url = kwargs.pop('base_url', RUZ_API_URL)
        if not self._url:
            raise PermissionError("Can't get base url!")
        self._endpoints = kwargs.pop('endpoints', RUZ_API_ENDPOINTS)
        self._url2 = self._url
        self._logger = Logger(str(self.__class__))
        if not strict_v1:
            self._url2 += r"v2/"
        super(RUZ, self).__init__()

    @property
    def v(self) -> int:
        '''
            Max API version

            >>> RUZ().v
            2
            >>> RUZ(strict_v1=True).v
            1
        '''
        return 2 if self._url2[-2] == "2" else 1

    def _make_url(self, endpoint: str, data: dict=None, v: int=1) -> str:
        ''' Creates full url for API requests '''
        url = self._url if v == 1 else self._url2
        if data:
            return "{}{}?{}".format(url, self._endpoints[endpoint],
                                    parse.urlencode(data).encode('utf-8'))
        return "{}{}".format(url, self._endpoints[endpoint])

    def _request(self, endpoint: str, data: dict=None) -> HTTPResponse:
        ''' Implements request to API with given params '''
        try:
            return request.urlopen(self._make_url(endpoint, data, v=2))
        except error.HTTPError as excinfo:
            self._logger.warning("v2 API unavailable: %s", excinfo)
        return request.urlopen(self._make_url(endpoint, data))

    def get(self, endpoint: str, **params) -> dict:
        ''' Return requested data in JSON '''
        try:
            response = self._request(endpoint, data=params)
            return json.loads(response.read().decode('utf-8'))
        except error.HTTPError as excinfo:
            self._logger.error(excinfo)
            return {}

    def schedule(self, from_date: str, to_date: str, email: str=None,
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
        return self.get("schedule", fromDate=from_date, toDate=to_date,
                        email=email, data=params)

    @lru_cache(maxsize=16)
    def groups(self, **params) -> dict:
        '''
            Return list of groups.

            :param facultyOid: int. Course ID.
            :param findText: str. Text to find.
        '''
        return self.get("groups", data=params)

    @lru_cache(maxsize=16)
    def staff_of_group(self, group_id: int, **params) -> dict:
        '''
            Return list of students in group.

            :param group_id: int, required. Group' ID.
            :param findText: str. Text to find.
        '''
        return self.get("staffOfGroup", groupOid=group_id, data=params)

    @lru_cache(maxsize=16)
    def streams(self, **params) -> dict:
        '''
            Return list of study streams.

            :param findText: str. Text to find.
        '''
        return self.get("streams", data=params)

    @lru_cache(maxsize=16)
    def staff_of_streams(self, stream_id: int, **params) -> dict:
        '''
            Return list of the groups on study stream.

            :param stream_id: int, required. Group' ID.
        '''
        return self.get("staffOfStreams", streamOid=stream_id, data=params)

    @lru_cache(maxsize=16)
    def lecturers(self, **params) -> dict:
        '''
            Return list of teachers.

            :param chairOid: int. ID of department.
            :param findText: str. Text to find.
        '''
        return self.get("lecturers", data=params)

    @lru_cache(maxsize=16)
    def auditoriums(self, **params) -> dict:
        '''
            Return list of auditoriums.

            :param buildingOid: int. ID of building.
            :param findText: str. Text to find.
        '''
        return self.get("auditoriums", data=params)

    @lru_cache(maxsize=1)
    def type_of_auditoriums(self) -> dict:
        ''' Return list of auditoriums' types. '''
        return self.get("typeOfAuditoriums")

    @lru_cache(maxsize=1)
    def kind_of_works(self) -> dict:
        ''' Return list of classes' types. '''
        return self.get("kindOfWorks")

    @lru_cache(maxsize=16)
    def buildings(self, **params) -> dict:
        '''
            Return list of buildings.

            :param findText: str. Text to find.
        '''
        return self.get("buildings", data=params)

    @lru_cache(maxsize=16)
    def faculties(self, **params) -> dict:
        '''
            Return list of learning programs (faculties).

            :param findText: str. Text to find.
        '''
        return self.get("faculties", data=params)

    @lru_cache(maxsize=16)
    def chairs(self, **params) -> dict:
        '''
            Return list of departments.

            :param facultyOid: int. ID of course (learning program).
            :param findText: str. Text to find.
        '''
        return self.get("chairs", data=params)

    @lru_cache(maxsize=16)
    def sub_groups(self, **params) -> dict:
        '''
            Return list of subgroups.

            :param findText: str. Text to find.
        '''
        return self.get("subGroups", data=params)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
