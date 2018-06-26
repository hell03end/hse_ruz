"""
    Python wrapper for HSE RUZ API.

    Usage
    -----
    import ruz
    assert ruz.person_lessons("mymail@edu.hse.ru")
"""

from ruz.api import (auditoriums, buildings, chairs, faculties, find_by_str,
                     groups, kind_of_works, lecturers, person_lessons,
                     schedules, staff_of_group, streams, sub_groups,
                     type_of_auditoriums)

__author__ = "Dmitriy Pchelkin | hell03end"
__version__ = (2, 1, 2)
