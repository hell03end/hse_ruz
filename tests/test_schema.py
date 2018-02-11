""" Test that current response schema is still actual """

from tests import TRUSTED_EMAILS, TRUSTED_GROUP_ID, logging

import ruz
from ruz.schema import RESPONSE_SCHEMA


def _test_schema(schema, response):
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
                    logging.debug("param::%s", key)
                    raise err
            # check missing keys (difference between schema and response)
            if element.keys() != schema.keys():
                if len(element.keys()) > len(schema.keys()):
                    missed_keys = set(element.keys()) - set(schema.keys())
                else:
                    missed_keys = set(schema.keys()) - set(element.keys())
                logging.warning("missed keys::%s", missed_keys)
    elif response and isinstance(response, dict):
        for key, value in response.items():
            _test_schema(schema[key], value)


# ===== API methods =====

def test_schedule():
    logging.warning("Trusted emails may be deactivated in few years!")
    _test_schema(schema=RESPONSE_SCHEMA['schedule'],
                 response=ruz.person_lessons(email=TRUSTED_EMAILS['student']))


def test_groups():
    _test_schema(schema=RESPONSE_SCHEMA['groups'], response=ruz.groups())


def test_staffOfGroup():
    logging.warning("Group id may be deactivated in few years!")
    _test_schema(schema=RESPONSE_SCHEMA['staffOfGroup'],
                 response=ruz.staff_of_group(group_id=TRUSTED_GROUP_ID))


def test_streams():
    _test_schema(schema=RESPONSE_SCHEMA['streams'], response=ruz.streams())


def test_lecturers():
    _test_schema(schema=RESPONSE_SCHEMA['lecturers'], response=ruz.lecturers())


def test_auditoriums():
    _test_schema(schema=RESPONSE_SCHEMA['auditoriums'],
                 response=ruz.auditoriums())


def test_typeOfAuditoriums():
    _test_schema(schema=RESPONSE_SCHEMA['typeOfAuditoriums'],
                 response=ruz.type_of_auditoriums())


def test_kindOfWorks():
    _test_schema(schema=RESPONSE_SCHEMA['kindOfWorks'],
                 response=ruz.kind_of_works())


def test_buildings():
    _test_schema(schema=RESPONSE_SCHEMA['buildings'], response=ruz.buildings())


def test_faculties():
    _test_schema(schema=RESPONSE_SCHEMA['faculties'], response=ruz.faculties())


def test_chairs():
    _test_schema(schema=RESPONSE_SCHEMA['chairs'], response=ruz.chairs())


def test_subGroups():
    _test_schema(schema=RESPONSE_SCHEMA['subGroups'],
                 response=ruz.sub_groups())
