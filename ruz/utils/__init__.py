import os

from .logging import Logger, LEVELS
from .schema import REQUEST_SCHEMA


RUZ_API_URL = os.environ.get("API_RUZ_URL")
RUZ_API_ENDPOINTS = {
    'schedule': "personLessons",
    'groups': "groups",
    'staffOfGroup': "staffOfGroup",
    'streams': "streams",
    'staffOfStreams': "staffOfStreams",
    'lecturers': "lecturers",
    'auditoriums': "auditoriums",
    'typeOfAuditoriums': "typeOfAuditoriums",
    'kindOfWorks': "kindOfWorks",
    'buildings': "buildings",
    'faculties': "faculties",
    'chairs': "chairs",
    'subGroups': "subGroups"
}
