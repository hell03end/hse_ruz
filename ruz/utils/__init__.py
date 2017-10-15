import os

from .logging import Logger, LEVELS
from .schema import REQUEST_SCHEMA, RESPONSE_SCHEMA


RUZ_API_URL = os.environ.get("API_RUZ_URL")
RUZ_API_ENDPOINTS = {
    'schedule': "personLessons",
    'groups': "groups",
    'staffOfGroup': "staffOfGroup",
    'staff_of_group': "staffOfGroup",
    'streams': "streams",
    'staffOfStreams': "staffOfStreams",
    'staff_of_streams': "staffOfStreams",
    'lecturers': "lecturers",
    'auditoriums': "auditoriums",
    'typeOfAuditoriums': "typeOfAuditoriums",
    'type_of_auditoriums': "typeOfAuditoriums",
    'kindOfWorks': "kindOfWorks",
    'kind_of_works': "kindOfWorks",
    'buildings': "buildings",
    'faculties': "faculties",
    'chairs': "chairs",
    'subGroups': "subGroups",
    'subgroups': "subGroups",
    'sub_groups': "subGroups"
}
