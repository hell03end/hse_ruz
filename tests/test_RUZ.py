import re
from time import sleep

import pytest
from ruz import EMAIL_DOMAINS, REQUEST_SCHEMA, RUZ
from ruz.utils import RUZ_API2_ENDPOINTS as RUZ_ENDPOINTS2
from ruz.utils import RUZ_API2_URL as RUZ_URL2
from ruz.utils import RUZ_API_ENDPOINTS as RUZ_ENDPOINTS
from ruz.utils import RUZ_API_URL as RUZ_URL
from ruz.utils.logging import Logger


class TestRUZ:
    def setup_class(self):
        self.api = RUZ(strict_v1=True)
        self.api2 = RUZ(strict_v1=False)
        self._logger = Logger(str(self.__class__))

    def setup_method(self):
        sleep(0.01)

    def _test_simple_endpoint(self, response: object,
                              resp_type: type=list) -> None:
        assert response is not None
        assert isinstance(response, resp_type)
        del response

    def _test_endpoint_with_kwargs(self, response: tuple,
                                   resp_type: type=(list, None)) -> None:
        assert response[0] is not None  # full response
        assert response[1] is not None  # response with arg
        assert response[2] is not None  # response with duplicated arg
        assert isinstance(response[0], resp_type)
        assert isinstance(response[1], resp_type)
        assert isinstance(response[2], resp_type)
        assert len(response[1]) < len(response[0])
        assert response[1] == response[2]
        del response

    def _test_endpoint_with_args(self, response: tuple,
                                 resp_type: type=(list, None)) -> None:
        assert response[0] is not None  # response with arg
        assert response[1] is not None  # response with duplicated arg
        assert isinstance(response[0], resp_type)
        assert isinstance(response[1], resp_type)
        assert response[0] == response[1]

    def test___init__(self):
        api = RUZ(
            base_url="123",
            endpoints={'a': 123},
            schema={'a': int},
            domains=('abc',)
        )
        assert api._url == "123"
        assert api._endpoints == {'a': 123}
        assert api._schema == {'a': int}
        assert api._domains == ('abc',)

        with pytest.raises(PermissionError) as excinfo:
            api = RUZ(base_url=123)
        assert excinfo
        for key in ("endpoints", "schema", "domains"):
            self._logger.debug("key::%s", key)
            with pytest.raises(ValueError) as excinfo:
                api = RUZ(**{key: 123})
            assert excinfo

    def test_ok(self):
        assert self.api.ok
        assert self.api2.ok

    def test_schema(self):
        assert self.api.schema == REQUEST_SCHEMA
        assert self.api.schema is not self.api.schema  # deepcopy
        assert self.api2.schema == REQUEST_SCHEMA
        assert self.api2.schema is not self.api.schema

    def test_v(self):
        assert self.api.v == 1
        assert self.api2.v == 2

    def test_domains(self):
        assert self.api.domains == EMAIL_DOMAINS
        assert isinstance(self.api.domains, tuple)
        assert self.api2.domains == EMAIL_DOMAINS
        assert isinstance(self.api2.domains, tuple)

    def test_endpoints(self):
        assert self.api.endpoints == RUZ_ENDPOINTS
        assert self.api.endpoints is not self.api.endpoints
        assert self.api2.endpoints == RUZ_ENDPOINTS
        assert self.api2.endpoints is not self.api.endpoints

    def test_is_student(self):
        assert not self.api.is_student("somemail@hse.ru")
        assert self.api.is_student("somemail@edu.hse.ru")
        with pytest.raises(ValueError) as excinfo:
            self.api.is_student(123)
        assert excinfo
        with pytest.raises(ValueError) as excinfo:
            self.api.is_student("somemail@gmail.com")
        assert excinfo

    def test__make_url(self):
        for key, endpoint in RUZ_ENDPOINTS.items():
            assert self.api._make_url(key) == RUZ_URL + endpoint
            assert self.api._make_url(key, v=2) == RUZ_URL + endpoint
            assert self.api2._make_url(key, v=1) == RUZ_URL + endpoint
        for key, endpoint in RUZ_ENDPOINTS2.items():
            assert self.api2._make_url(key, v=2) == RUZ_URL2 + endpoint
        with pytest.raises(KeyError):
            self.api._make_url("")

    # TODO
    def test__request(self) -> NotImplemented:
        return NotImplemented

    # TODO: test all cases (type of param, etc.)
    def test__verify_schema(self):
        with pytest.raises(KeyError) as excinfo:
            self.api._verify_schema("")
        assert excinfo
        for endpoint in RUZ_ENDPOINTS:
            if endpoint == 'schedule':
                with pytest.raises(ValueError) as excinfo:
                    self.api._verify_schema(endpoint, email="123")
                assert excinfo
                with pytest.raises(ValueError) as excinfo:
                    self.api._verify_schema(endpoint)
                assert excinfo
            else:
                with pytest.raises(KeyError) as excinfo:
                    self.api._verify_schema(endpoint, tmp=None)
                assert excinfo
                assert not self.api._verify_schema(endpoint)

    def test_check_email(self):
        correct_emails = ("somemail@edu.hse.ru", "somemail@hse.ru")
        incorrect_emails = ("somemail@hse.com", "somem@il@edu.hse.ru",
                            "somemail@google.ru")
        for email in incorrect_emails:
            with pytest.raises(ValueError) as excinfo:
                self.api.check_email(email)
            assert excinfo
        for email in correct_emails:
            assert self.api.check_email(email) is None

    def test_date(self):
        with pytest.raises(ValueError) as excinfo:
            self.api.date(3.14)
        assert excinfo
        assert isinstance(self.api.date(), str)
        assert len(self.api.date()) == 10
        assert re.match(r"[\d]{4}\.[\d]{2}\.[\d]{2}", self.api.date())
        assert self.api.date(-1) < self.api.date()
        assert self.api.date(1) > self.api.date(0)

    # DANGEROUS: email will be deactivated in few years
    def test_verify_email(self):
        correct_emails = ("somemail@edu.hse.ru", "somemail@hse.ru")
        incorrect_emails = ("somemail@hse.com", "somem@il@edu.hse.ru",
                            "somemail@google.ru")
        # offline
        for email in incorrect_emails:
            with pytest.raises(ValueError) as excinfo:
                self.api.verify_email(email, check_online=False)
            assert excinfo
        for email in correct_emails:
            assert self.api.verify_email(email, check_online=False) is None
        with pytest.raises(ValueError) as excinfo:
            self.api.verify_email(correct_emails[0], receiver_type=-1,
                                  check_online=False)
        assert excinfo
        with pytest.raises(ValueError) as excinfo:
            self.api.verify_email(correct_emails[0], receiver_type=2,
                                  check_online=False)
        assert excinfo
        # online
        for email in correct_emails:
            with pytest.raises(ValueError) as excinfo:
                self.api.verify_email(email, check_online=True)
            assert excinfo
        assert self.api.verify_email("dapchelkin@edu.hse.ru") is None

    # TODO: test all cases (safe key, None kwargs, etc.)
    def test__get(self):
        incorrect_email = "somemail@hse.com"
        for endpoint in RUZ_ENDPOINTS:
            if endpoint == "schedule":
                with pytest.raises(ValueError) as excinfo:
                    self.api._get(endpoint, email=incorrect_email)
                assert excinfo
            else:
                with pytest.raises(KeyError) as excinfo:
                    self.api._get(endpoint, tmp=123)
                assert excinfo
        assert self.api._get("kind_of_works")

    def test__map_schedules(self):
        assert isinstance(self.api._map_schedules("email", ("123",)), map)
        assert self.api._map_schedules("email", "123", allowed_types=(str,))
        assert self.api._map_schedules("email", 123, allowed_types=(int,))
        with pytest.raises(ValueError) as excinfo:
            self.api._map_schedules("email", "123", allowed_types=(int,))
        assert excinfo

    # TODO: test auditoriums and students
    def test_schedules(self):
        with pytest.raises(ValueError) as excinfo:
            self.api.schedules()
        assert excinfo
        assert isinstance(self.api.schedules(emails=["abc"]), map)
        assert next(self.api.schedules(emails="dapchelkin@edu.hse.ru",
                                       safe=False)) is not None
        assert self.api.schedules(lecturer_ids=[6232], safe=False)

    # DANGEROUS: email will be deactivated in few years
    # TODO: test auditorium_id, student_id, lecturer_id keys
    def test_person_lessons(self):
        student_email = "dapchelkin@edu.hse.ru"
        lecturer_email = "aromanov@hse.ru"
        incorrect_email = "somemail@hse.ru"
        self._test_endpoint_with_args((
            self.api.person_lessons(lecturer_email),
            self.api.person_lessons(lecturer_email, receiver_type=1)
        ))
        assert self.api.person_lessons(student_email) is not None
        assert self.api.person_lessons(incorrect_email, safe=True,
                                       check_online=False) is not None
        assert self.api.person_lessons(incorrect_email, safe=False,
                                       check_online=False) is None
        with pytest.raises(ValueError) as excinfo:
            self.api.person_lessons(incorrect_email, check_online=True)
        assert excinfo
        for lecturer_id in (24577, 19000, 24187, 23867, 22349):
            self._test_simple_endpoint(
                self.api.person_lessons(lecturer_id=lecturer_id, safe=False)
            )

    def test_groups(self):
        self._test_endpoint_with_kwargs((
            self.api.groups(),
            self.api.groups(faculty_id=5490),
            self.api.groups(faculty_id=5577, facultyOid=5490)
        ))

    def test_staff_of_group(self):
        self._test_endpoint_with_args((
            self.api.staff_of_group(group_id=7699),
            self.api.staff_of_group(group_id=1, groupOid=7699)
        ))

    def test_streams(self):
        self._test_simple_endpoint(self.api.streams())

    def test_staff_of_streams(self):
        self._test_endpoint_with_args((
            self.api.staff_of_streams(stream_id=45771),
            self.api.staff_of_streams(stream_id=1, streamOid=45771)
        ))

    def test_lecturers(self):
        self._test_endpoint_with_kwargs((
            self.api.lecturers(),
            self.api.lecturers(chair_id=1166),
            self.api.lecturers(chair_id=1146, chairOid=1166)
        ))

    def test_auditoriums(self):
        self._test_endpoint_with_kwargs((
            self.api.auditoriums(),
            self.api.auditoriums(building_id=2272),
            self.api.auditoriums(building_id=2222, buildingOid=2272)
        ))

    def test_type_of_auditoriums(self):
        self._test_simple_endpoint(self.api.type_of_auditoriums())

    def test_kind_of_works(self):
        self._test_simple_endpoint(self.api.kind_of_works())

    def test_buildings(self):
        self._test_simple_endpoint(self.api.buildings())

    def test_faculties(self):
        self._test_simple_endpoint(self.api.faculties())

    def test_chairs(self):
        self._test_endpoint_with_kwargs((
            self.api.chairs(),
            self.api.chairs(faculty_id=5490),
            self.api.chairs(faculty_id=5577, facultyOid=5490)
        ))

    def test_sub_groups(self):
        self._test_simple_endpoint(self.api.sub_groups())
