import json
import re
from enum import Enum
from typing import Any


# Convert keys to camel case
def _to_camel_case(string: str) -> str:
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), string)


# Enums must be managed in a particular way: their json representation should be just their value
def _manage_enums(o: Any):
    return o.value if isinstance(o, Enum) else o


# Get the fields of the object
def _get_fields(o: Any, camel_case: bool = False) -> dict:
    return {k if not camel_case else _to_camel_case(k): _manage_enums(v) for k, v in vars(o).items()}


# Convert object to JSON string representation
def to_direct_json(obj: Any, camel_case: bool = False) -> str:
    # Use "vars" function, but make field camel case!
    args = {"default": lambda o: _get_fields(o, camel_case=camel_case), "indent": 4}
    return json.dumps(obj, **args)
