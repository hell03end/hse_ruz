import os


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

LEVELS = {
    "NOTSET": 0,
    "DEBUG": 10,
    "INFO": 20,
    "WARN": 30,
    "WARNING": 30,
    "ERROR": 40,
    "FATAL": 50,
    "CRITICAL": 50
}


def Logger(name: str, level: int=LEVELS["DEBUG"], **kwargs) -> ...:
    import logging
    logging.basicConfig(
        format=kwargs.get(
            "format",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ),
        level=level
    )
    return logging.getLogger(name)
