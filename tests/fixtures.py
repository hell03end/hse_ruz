# DANGEROUS: trusted fixtures may be deactivated in few years!

TRUSTED_EMAILS = {
    'student': r"dapchelkin@edu.hse.ru",
    'lecturer': r"aromanov@hse.ru"
}
NON_TRUSTED_EMAILS = {
    'other': r"hell03end@outlook.com",
    'hse': r"hell03end@hse.ru"
}
TRUSTED_GROUP_ID = 7699
TRUSTED_LECTURER_ID = 6232

SAMPLE_SCHEDULE = [
    {
        'date': '2018.06.07',
        'dayOfWeek': 4
    },
    {
        'date': '2018.06.08',
        'dayOfWeek': 5
    },
    {
        'date': '2018.06.08',
        'dayOfWeek': 5
    },
    {
        'date': '2018.06.11',
        'dayOfWeek': 1
    },
    {
        'date': '2018.06.11',
        'dayOfWeek': 1
    }
]
SPLITED_SCHEDULE = [
    {
        'date': '2018.06.07',
        'dayOfWeek': 4,
        'count': 1,
        'lessons': [
            {
                'date': '2018.06.07',
                'dayOfWeek': 4
            }
        ]
    },
    {
        'date': '2018.06.08',
        'dayOfWeek': 5,
        'count': 2,
        'lessons': [
            {
                'date': '2018.06.08',
                'dayOfWeek': 5
            },
            {
                'date': '2018.06.08',
                'dayOfWeek': 5
            }
        ]
    },
    {
        'date': '2018.06.11',
        'dayOfWeek': 1,
        'count': 2,
        'lessons': [
            {
                'date': '2018.06.11',
                'dayOfWeek': 1
            },
            {
                'date': '2018.06.11',
                'dayOfWeek': 1
            }
        ]
    }
]
