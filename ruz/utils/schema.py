import pickle
import os


def load_dump(path: str) -> object:
    ''' load object from pickle dump '''
    if os.path.exists(path):
        with open(path, 'rb') as reader:
            return pickle.load(reader)


def save_dump(path: str, obj: object, rewrite: bool=False) -> bool:
    ''' save object to pickle dump '''
    if not os.path.exists(path) or rewrite:
        with open(path, 'wb') as writer:
            pickle.dump(obj, writer)
            return True
    return False


def recreate_dump(force: bool=False) -> None:
    ''' create new dump files '''
    if not os.path.exists(DUMPS_PATH) or force:
        from .raw_schema import (REQUEST_SCHEMA, RESPONSE_SCHEMA,
                                 RUZ_API_ENDPOINTS)

        if not os.path.exists(DUMPS_PATH):
            os.makedirs(DUMPS_PATH)
        save_dump(REQ_DUMP_PATH, REQUEST_SCHEMA, rewrite=True)
        save_dump(RESP_DUMP_PATH, RESPONSE_SCHEMA, rewrite=True)
        save_dump(ENDPOINTS_DUMP_PATH, RUZ_API_ENDPOINTS, rewrite=True)


DUMPS_PATH = os.path.join(os.path.dirname(__file__), "dumps")
REQ_DUMP_PATH = os.path.join(DUMPS_PATH, "REQUEST_SCHEMA.dump")
RESP_DUMP_PATH = os.path.join(DUMPS_PATH, "RESPONSE_SCHEMA.dump")
ENDPOINTS_DUMP_PATH = os.path.join(DUMPS_PATH, "RUZ_API_ENDPOINTS.dump")


recreate_dump()


REQUEST_SCHEMA = load_dump(REQ_DUMP_PATH)
assert REQUEST_SCHEMA

RESPONSE_SCHEMA = load_dump(RESP_DUMP_PATH)
assert RESPONSE_SCHEMA

RUZ_API_ENDPOINTS = load_dump(ENDPOINTS_DUMP_PATH)
assert RUZ_API_ENDPOINTS


__all__ = ("REQUEST_SCHEMA", "RESPONSE_SCHEMA", "RUZ_API_ENDPOINTS")


if __name__ == "__main__":
    recreate_dump(force=True)
