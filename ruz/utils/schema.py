REQUEST_SCHEMA = {
    'schedule': {
        'from_date': str,
        'fromDate': str,
        'to_date': str,
        'toDate': str,
        'receiverType': int,
        'groupOid': int,
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
    'subGroups': {'findText': str}
}


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
            'group': None,
            'groupOid': int,
            'isBan': bool,
            'kindOfWork': str,
            'lecturer': str,
            'lecturerOid': int,
            'stream': str,
            'streamOid': int,
            'subGroup': None,
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
                'group': None,
                'groupOid': int,
                'isBan': bool,
                'kindOfWork': str,
                'lecturer': str,
                'lecturerOid': int,
                'stream': str,
                'streamOid': int,
                'subGroup': None,
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
    'staffOfStreams': {},
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
            'code': str,
            'name': str,
            'typeOfAuditoriumOid': int
        }
    ],
    'kindOfWorks': [
        {
            'abbr': str,
            'code': None,
            'complexity': int,
            'kindOfWorkOid': int,
            'name': str,
            'unit': str
        }
    ],
    'buildings': [
        {
            'abbr': str,
            'address': str,
            'buildingOid': int,
            'name': str
        }
    ],
    'faculties': [
        {
            'abbr': str,
            'code': None,
            'facultyOid': int,
            'institute': str,
            'name': str
        }
    ],
    'chairs': [
        {
            'abbr': str,
            'chairOid': int,
            'code': str,
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
