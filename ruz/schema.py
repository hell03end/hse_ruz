import os

API_URL = os.environ.get("HSE_RUZ_API_URL",
                         r"http://92.242.58.221/ruzservice.svc/")

# detect RUZ API version from possible RUZ API URLs
API_V = 1
if API_URL == r"http://92.242.58.221/ruzservice.svc/v2/":
    API_V = 2
elif API_URL == r"https://www.hse.ru/api/":
    API_V = 3

# collection of API endpoints and their aliases
API_ENDPOINTS = {
    'schedule': r"personLessons",
    'lessons': r"personLessons",
    'person_lessons': r"personLessons",
    'personLessons': r"personLessons",
    'groups': r"groups",
    'staffOfGroup': r"staffOfGroup",
    'staff_of_group': r"staffOfGroup",
    'streams': r"streams",
    'staffOfStreams': r"staffOfStreams",
    'staff_of_streams': r"staffOfStreams",
    'lecturers': r"lecturers",
    'auditoriums': r"auditoriums",
    'typeOfAuditoriums': r"typeOfAuditoriums",
    'type_of_auditoriums': r"typeOfAuditoriums",
    'kindOfWorks': r"kindOfWorks",
    'kind_of_works': r"kindOfWorks",
    'buildings': r"buildings",
    'faculties': r"faculties",
    'chairs': r"chairs",
    'subGroups': r"subGroups",
    'subgroups': r"subGroups",
    'sub_groups': r"subGroups"
}
if API_V == 3:
    API_ENDPOINTS = {
        'schedule': r"timetable/lessons",
        'lessons': r"timetable/lessons",
        'person_lessons': r"timetable/lessons",
        'personLessons': r"timetable/lessons"
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
            'auditoriumGid': int,
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
            'groupGid': int,
            'isBan': bool,
            'kindOfWork': str,
            'lecturer': str,
            'lecturerOid': int,
            'lecturerGid': int,
            'stream': str,
            'streamOid': int,
            'streamGid': int,
            'subGroup': (str, type(None)),
            'subGroupOid': int,
            'subGroupGid': int
        }
    ],
    'schedule2': {
        'Count': int,
        'Lessons': [
            {
                'auditorium': str,
                'auditoriumOid': int,
                'auditoriumGid': int,
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
                'groupGid': int,
                'isBan': bool,
                'kindOfWork': str,
                'lecturer': str,
                'lecturerOid': int,
                'lecturerGid': int,
                'stream': str,
                'streamOid': int,
                'streamGid': int,
                'subGroup': (str, type(None)),
                'subGroupOid': int,
                'subGroupGid': int
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
            'chairGid': int,
            'course': int,
            'faculty': str,
            'facultyOid': int,
            'facultyGid': int,
            'formOfEducation': str,
            'groupOid': int,
            'groupGid': int,
            'kindEducation': int,
            'number': str,
            'speciality': str,
            'FormOfEducationGid': int,
            'FormOfEducationOid': int,
            'SpecialityGid': int,
            'SpecialityOid': int
        }
    ],
    'staffOfGroup': [
        {
            'fio': str,
            'shortFIO': str,
            'studentOid': int,
            'studentGid': int
        }
    ],
    'streams': [
        {
            'abbr': str,
            'course': str,
            'faculty': str,
            'facultyOid': int,
            'facultyGid': int,
            'formOfEducation': str,
            'name': str,
            'streamOid': int,
            'streamGid': int,
            'yearOfEducation': int,
            'FormOfEducationGid': int,
            'FormOfEducationOid': int
        }
    ],
    'staffOfStreams': [
        {
            "GroupNumber": str,
            "GroupOid": int,
            "GroupGid": int,
            "SubgroupName": str,
            "SubgroupOid": int,
            "SubgroupGid": int
        }
    ],
    'lecturers': [
        {
            'chair': str,
            'chairOid': int,
            'chairGid': int,
            'fio': str,
            'lecturerOid': int,
            'lecturerGid': int,
            'shortFIO': str
        }
    ],
    'auditoriums': [
        {
            'auditoriumOid': int,
            'auditoriumGid': int,
            'building': str,
            'buildingOid': int,
            'buildingGid': int,
            'number': str,
            'typeOfAuditorium': str,
            'TypeOfAuditoriumOid': int
        }
    ],
    'typeOfAuditoriums': [
        {
            'abbr': str,
            'code': (str, type(None)),
            'name': str,
            'typeOfAuditoriumOid': int,
            'hideincapacity': int,
            'TypeOfAuditoriumGid': int
        }
    ],
    'kindOfWorks': [
        {
            'abbr': str,
            'code': (str, type(None)),
            'complexity': int,
            'kindOfWorkOid': int,
            'kindOfWorkGid': int,
            'name': str,
            'unit': str
        }
    ],
    'buildings': [
        {
            'abbr': str,
            'address': (str, type(None)),
            'buildingOid': int,
            'buildingGid': int,
            'name': str
        }
    ],
    'faculties': [
        {
            'abbr': str,
            'code': (str, type(None)),
            'facultyOid': int,
            'facultyGid': int,
            'institute': str,
            'name': str
        }
    ],
    'chairs': [
        {
            'abbr': (str, type(None)),
            'chairOid': int,
            'chairGid': int,
            'code': (str, type(None)),
            'faculty': str,
            'facultyOid': int,
            'facultyGid': int,
            'name': str
        }
    ],
    'subGroups': [
        {
            'abbr': str,
            'group': str,
            'groupOid': int,
            'groupGid': int,
            'name': str,
            'subGroupOid': int,
            'subgroupGid': int
        }
    ]
}
