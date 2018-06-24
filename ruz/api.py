import logging
from collections import Callable, Iterable
from functools import lru_cache

from ruz.utils import get, get_formated_date, is_student


def schedules(emails: Iterable=None,
              lecturer_ids: Iterable=None,
              auditorium_ids: Iterable=None,
              student_ids: Iterable=None,
              **params) -> map:
    """
        Classes schedule for multiply students/lecturers as generator

        See RUZ::person_lessons for more details.
        One of the followed required: lecturer_ids, auditorium_ids,
            student_ids, emails. Throw an exception.

        :param emails - emails on hse.ru (edu.hse.ru for students).
        :param lecturer_ids - IDs of teacher.
        :param auditorium_ids - IDs of auditorium.
        :param student_ids - IDs of student.
    """
    def get_handler(key: str) -> Callable:
        def func(val: dict) -> list or dict:
            return person_lessons(**{key: val}, **params)
        return func

    if emails:
        return map(get_handler("email"), emails)
    elif lecturer_ids:
        return map(get_handler("lecturer_id"), lecturer_ids)
    elif auditorium_ids:
        return map(get_handler("auditorium_id"), auditorium_ids)
    elif student_ids:
        return map(get_handler("student_id"), student_ids)

    raise ValueError("One of the followed required: lecturer_ids, "
                     "auditorium_ids, student_ids, emails")


def person_lessons(email: str=None,
                   from_date: str=get_formated_date(),
                   to_date: str=get_formated_date(6),  # one week
                   receiver_type: int=None,
                   lecturer_id: int=None,
                   auditorium_id: int=None,
                   student_id: int=None,
                   **params) -> list:
    """
        Return classes schedule (for week by default)

        Automatically choose receiver type from given email address.
        There is no need to specify receiver type for students explicitly.
        One of the followed required: lecturer_id, auditorium_id,
            student_id, email. Throws an exception.
        Default values (fromDate, toDate) are set to return schedule for
            one week from now.

        :param email - email on hse.ru (edu.hse.ru for students).
        :param from_date, required - start of the period YYYY.MM.DD.
        :param to_date, required - end of the period YYYY.MM.DD.
        :param receiver_type - type of the schedule
            (1/2/3 for teacher/auditorium/student).
        :param lecturer_id - ID of teacher.
        :param auditorium_id - ID of auditorium.
        :param student_id - ID of student.
        :param check_online :type bool - online verification for email.
        :param safe :type bool - return something even if no data received.
    """
    if receiver_type is None:
        if email is not None and not is_student(email):
            logging.debug("Detect lecturer email: '%s'.", email)
            receiver_type = 1
        elif lecturer_id is not None:
            logging.debug("Detect lecturer %d.", lecturer_id)
            receiver_type = 1
        elif auditorium_id is not None:
            logging.debug("Detect auditorium %d.", auditorium_id)
            receiver_type = 2
    elif receiver_type == 3:
        receiver_type = None

    return get(
        "schedule",
        fromDate=from_date,
        toDate=to_date,
        email=email,
        receiverType=receiver_type,
        lecturerOid=lecturer_id,
        auditoriumOid=auditorium_id,
        studentOid=student_id,
        **params
    )


def groups(faculty_id: int=None) -> list:
    """
        Return collection of groups

        :param faculty_id - course ID.
    """
    return get("groups", facultyOid=faculty_id)


def staff_of_group(group_id: int) -> list:
    """
        Return collection of students in group

        :param group_id, required - group' ID.
    """
    return get("staffOfGroup", groupOid=group_id)


@lru_cache(maxsize=1)
def streams(reset_cache: bool=False) -> list:
    """
        Return collection of study streams

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("streams")


def lecturers(chair_id: int=None) -> list:
    """
        Return collection of teachers

        :param chair_id - ID of department.
    """
    return get("lecturers", chairOid=chair_id)


def auditoriums(building_id: int=None) -> list:
    """
        Return collection of auditoriums

        :param building_id - ID of building.
    """
    return get("auditoriums", buildingOid=building_id)


@lru_cache(maxsize=1)
def type_of_auditoriums(reset_cache: bool=False) -> list:
    """
        Return collection of auditoriums' types

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("typeOfAuditoriums")


@lru_cache(maxsize=1)
def kind_of_works(reset_cache: bool=False) -> list:
    """
        Return collection of classes' types

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("kindOfWorks")


@lru_cache(maxsize=1)
def buildings(reset_cache: bool=False) -> list:
    """
        Return collection of buildings

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("buildings")


@lru_cache(maxsize=1)
def faculties(reset_cache: bool=False) -> list:
    """
        Return collection of learning programs

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("faculties")


def chairs(faculty_id: int=None) -> list:
    """
        Return collection of departments

        :param faculty_id - ID of course (learning program).
    """
    return get("chairs", facultyOid=faculty_id)


@lru_cache(maxsize=1)
def sub_groups(reset_cache: bool=False) -> list:
    """
        Return collection of subgroups

        Cache requested values.
        :param reset - use to reset cached value.
    """
    return get("subGroups")


def find_by_str(subject: str or Callable,
                query: str,
                by: str="name",
                **params) -> list:
    """
        Linear search for subject by given text field (as query)

        Search method is very straightforward. For more complex searches
        use custom implementation.
        Throws an exception:
            * KeyError if no subject found.
            * NotImplementedError if method is not implemented for subject.

        :param subject - subject to find: possible variants:
            * buildings: 'name', 'address', 'abbr';
            * faculties: 'name', 'institute', 'abbr';
            * sub_groups: 'name', 'group', 'abbr';
            * streams: 'name', 'faculty', 'abbr', 'formOfEducation', 'course';
            * type_of_auditoriums: 'name', 'abbr';
            * kind_of_works: 'name', 'abbr';
            * chairs: 'name', 'faculty', 'abbr';
            * auditoriums: 'number', 'building', 'typeOfAuditorium';
            * lecturers: 'chair', 'fio', 'shortFIO';
            * groups: 'faculty', 'formOfEducation', 'number', 'speciality';
            * staff_of_group: 'fio', 'shortFIO';
            * person_lessons: 'building', 'date', 'beginLesson', 'auditorium',
                'dateOfNest', 'dayOfWeekString', 'detailInfo', 'discipline',
                'disciplineinplan', 'endLesson', 'kindOfWork', 'lecturer',
                'stream'.
        :param query - text query to find.
        :param by - search field.
    """
    SUBJECTS = {
        buildings.__name__: buildings,
        faculties.__name__: faculties,
        sub_groups.__name__: sub_groups,
        streams.__name__: streams,
        type_of_auditoriums.__name__: type_of_auditoriums,
        kind_of_works.__name__: kind_of_works,
        chairs.__name__: chairs,
        auditoriums.__name__: auditoriums,
        lecturers.__name__: lecturers,
        groups.__name__: groups,
        staff_of_group.__name__: staff_of_group,
        person_lessons.__name__: person_lessons
    }

    if not isinstance(subject, Callable):
        subject = SUBJECTS[subject]
    elif subject.__name__ not in SUBJECTS.keys():
        raise NotImplementedError(subject.__name__)

    query = query.strip().lower()
    return [el for el in subject(**params)
            if query in (el[by].lower().strip() if el[by] else "")]
