# collection of API endpoints (and their aliases)
RUZ_API_ENDPOINTS = {
    'schedule': "personLessons",
    'lessons': "personLessons",
    'person_lessons': "personLessons",
    'personLessons': "personLessons",
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

# type rules to make request for API
REQUEST_SCHEMA = {
    'personLessons': {
        'from_date': str,
        'fromDate': str,
        'to_date': str,
        'toDate': str,
        'receiverType': int,
        'groupOid': int,  # depreciated
        'lecturerOid': int,
        'auditoriumOid': int,
        'studentOid': int,
        'email': str
    },
    'groups': {
        'facultyOid': int,
        'findText': str
    },
    'staffOfGroup': {
        'group_id': int,
        'groupOid': int,
        'findText': str
    },
    'streams': {'findText': str},
    'staffOfStreams': {
        'streamOid': int,
        'stream_id': int
    },
    'lecturers': {
        'chairOid': int,
        'findText': str
    },
    'auditoriums': {
        'buildingOid': int,
        'findText': str
    },
    'typeOfAuditoriums': {},
    'kindOfWorks': {},
    'buildings': {'findText': str},
    'faculties': {'findText': str},
    'chairs': {
        'facultyOid': int,
        'findText': str
    },
    'subGroups': {'findText': str},
    'subgroups': {'findText': str}
}
# type rules for correct response from API
RESPONSE_SCHEMA = {
    'schedule': [
        {
            'auditorium': str,
            'auditoriumOid': int,
            'beginLesson': str,
            'building': str,
            'date': str,
            'dateOfNest': str,
            'dayOfWeek': int,
            'dayOfWeekString': str,
            'detailInfo': str,
            'discipline': str,
            'disciplineinplan': str,
            'disciplinetypeload': int,
            'endLesson': str,
            'group': (str, type(None)),
            'groupOid': int,
            'isBan': bool,
            'kindOfWork': str,
            'lecturer': str,
            'lecturerOid': int,
            'stream': str,
            'streamOid': int,
            'subGroup': (str, type(None)),
            'subGroupOid': int
        }
    ],
    'schedule2': {
        'Count': int,
        'Lessons': [
            {
                'auditorium': str,
                'auditoriumOid': int,
                'beginLesson': str,
                'building': str,
                'date': str,
                'dateOfNest': str,
                'dayOfWeek': int,
                'dayOfWeekString': str,
                'detailInfo': str,
                'discipline': str,
                'disciplineinplan': str,
                'disciplinetypeload': int,
                'endLesson': str,
                'group': (str, type(None)),
                'groupOid': int,
                'isBan': bool,
                'kindOfWork': str,
                'lecturer': str,
                'lecturerOid': int,
                'stream': str,
                'streamOid': int,
                'subGroup': (str, type(None)),
                'subGroupOid': int
            }
        ],
        'StatusCode': {
            'Code': int,
            'Description': str
        }
    },  # api v2
    'groups': [
        {
            'chairOid': int,
            'course': int,
            'faculty': str,
            'facultyOid': int,
            'formOfEducation': str,
            'groupOid': int,
            'kindEducation': int,
            'number': str,
            'speciality': str
        }
    ],
    'staffOfGroup': [
        {
            'fio': str,
            'shortFIO': str,
            'studentOid': int
        }
    ],
    'streams': [
        {
            'abbr': str,
            'course': str,
            'faculty': str,
            'facultyOid': int,
            'formOfEducation': str,
            'name': str,
            'streamOid': int,
            'yearOfEducation': int
        }
    ],
    'staffOfStreams': [
        {
            "GroupNumber": str,
            "GroupOid": int,
            "SubgroupName": str,
            "SubgroupOid": int
        }
    ],
    'lecturers': [
        {
            'chair': str,
            'chairOid': int,
            'fio': str,
            'lecturerOid': int,
            'shortFIO': str
        }
    ],
    'auditoriums': [
        {
            'auditoriumOid': int,
            'building': str,
            'buildingOid': int,
            'number': str,
            'typeOfAuditorium': str
        }
    ],
    'typeOfAuditoriums': [
        {
            'abbr': str,
            'code': (str, type(None)),
            'name': str,
            'typeOfAuditoriumOid': int
        }
    ],
    'kindOfWorks': [
        {
            'abbr': str,
            'code': (str, type(None)),
            'complexity': int,
            'kindOfWorkOid': int,
            'name': str,
            'unit': str
        }
    ],
    'buildings': [
        {
            'abbr': str,
            'address': (str, type(None)),
            'buildingOid': int,
            'name': str
        }
    ],
    'faculties': [
        {
            'abbr': str,
            'code': (str, type(None)),
            'facultyOid': int,
            'institute': str,
            'name': str
        }
    ],
    'chairs': [
        {
            'abbr': (str, type(None)),
            'chairOid': int,
            'code': (str, type(None)),
            'faculty': str,
            'facultyOid': int,
            'name': str
        }
    ],
    'subGroups': [
        {
            'abbr': str,
            'group': str,
            'groupOid': int,
            'name': str,
            'subGroupOid': int
        }
    ]
}
