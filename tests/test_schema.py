""" Test current response schema is still actual """

from ruz import RUZ
from ruz.utils import RESPONSE_SCHEMA
from ruz.utils.logging import Logger


class TestResponseSchema:
    def setup_class(self):
        self.api = RUZ(strict_v1=True)
        self.api2 = RUZ(strict_v1=False)
        self._logger = Logger(str(self.__class__))

    def _test_schema(self, schema, response):
        if isinstance(schema, type):
            assert isinstance(response, schema)
        else:
            assert isinstance(response, type(schema))

        if response and isinstance(response, list):
            schema = schema[0]  # schema describe only one element
            for element in response:
                assert isinstance(element, type(schema))
                for key, value in element.items():
                    try:
                        assert isinstance(value, schema[key])
                    except AssertionError as err:
                        self._logger.debug("param::%s", key)
                        raise err
                # check missing keys (difference between schema and response)
                if element.keys() != schema.keys():
                    if len(element.keys()) > len(schema.keys()):
                        missed_keys = set(element.keys()) - set(schema.keys())
                    else:
                        missed_keys = set(schema.keys()) - set(element.keys())
                    self._logger.warning("missed keys::%s", missed_keys)
        elif response and isinstance(response, dict):
            for key, value in response.items():
                self._test_schema(schema[key], value)

    # DANGEROUS: email will be deactivated in few years
    def test_schedule(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['schedule'],
            response=self.api.person_lessons(email="dapchelkin@edu.hse.ru")
        )

    # DANGEROUS: email will be deactivated in few years
    def test_schedule2(self) -> NotImplemented:
        self._test_schema(
            schema=RESPONSE_SCHEMA['schedule2'],
            response=self.api2.person_lessons(email="dapchelkin@edu.hse.ru")
        )

    def test_groups(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['groups'],
            response=self.api.groups()
        )

    # DANGEROUS: group id may be deactivated in few years
    def test_staffOfGroup(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['staffOfGroup'],
            response=self.api.staff_of_group(group_id=7699)
        )

    def test_streams(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['streams'],
            response=self.api.streams()
        )

    # DANGEROUS: stream id may be deactivated in few years
    def test_staffOfStreams(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['staffOfStreams'],
            response=self.api.staff_of_streams(stream_id=0)
        )

    def test_lecturers(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['lecturers'],
            response=self.api.lecturers()
        )

    def test_auditoriums(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['auditoriums'],
            response=self.api.auditoriums()
        )

    def test_typeOfAuditoriums(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['typeOfAuditoriums'],
            response=self.api.type_of_auditoriums()
        )

    def test_kindOfWorks(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['kindOfWorks'],
            response=self.api.kind_of_works()
        )

    def test_buildings(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['buildings'],
            response=self.api.buildings()
        )

    def test_faculties(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['faculties'],
            response=self.api.faculties()
        )

    def test_chairs(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['chairs'],
            response=self.api.chairs()
        )

    def test_subGroups(self):
        self._test_schema(
            schema=RESPONSE_SCHEMA['subGroups'],
            response=self.api.sub_groups()
        )
