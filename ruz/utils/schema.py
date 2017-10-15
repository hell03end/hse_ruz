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


DUMPS_PATH = os.path.join(os.path.dirname(__file__), "dumps")
REQ_DUMP_PATH = os.path.join(DUMPS_PATH, "REQUEST_SCHEMA.dump")
RESP_DUMP_PATH = os.path.join(DUMPS_PATH, "RESPONSE_SCHEMA.dump")


REQUEST_SCHEMA = load_dump(REQ_DUMP_PATH)
assert REQUEST_SCHEMA

RESPONSE_SCHEMA = load_dump(RESP_DUMP_PATH)
assert RESPONSE_SCHEMA


__all__ = ("REQUEST_SCHEMA", "RESPONSE_SCHEMA")


if __name__ == "__main__":
    from .raw_schema import REQUEST_SCHEMA, RESPONSE_SCHEMA
    save_dump(REQ_DUMP_PATH, REQUEST_SCHEMA, rewrite=False)
    save_dump(RESP_DUMP_PATH, RESPONSE_SCHEMA, rewrite=False)
