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
        'findText': str
    },
    'streams': {'findText': str},
    'staffOfStreams': {'stream_id': int},
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
}
