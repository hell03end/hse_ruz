from ruz import RUZ, RESPONSE_SCHEMA


def test_schema():
    api = RUZ()
    schema = RESPONSE_SCHEMA['schedule']
    schedule = api.schedule("dapchelkin@edu.hse.ru")  # DANGEROUS
    assert isinstance(schedule, type(schema))
    if schedule:
        assert isinstance(schedule[0], type(schema[0]))
        for key, param in schedule[0].items():
            if param:
                assert isinstance(param, schema[0][key])
