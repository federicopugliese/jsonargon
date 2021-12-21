import typing
from typing import Any

from jsonargon.fields.dict import _StringDictField
from jsonargon.fields.list import _ListField
from jsonargon.fields.simple import JSONCLASS_DECORATED
from jsonargon.serialization.dictionary import to_direct_json


def to_json(obj: Any) -> str:

    # Build the dictionary from the object
    dictionary = to_dict(obj)

    # Dictionary -> string with the proper format
    return to_direct_json(dictionary, camel_case=False)


def to_dict(obj: Any) -> dict:

    dictionary = {}

    # Inspect the object
    cls = type(obj)
    annotations = typing.get_type_hints(cls)
    for attribute, metadata in annotations.items():

        # Get the value of that attribute (if it's a nested serializable class, do this recursively)
        value = getattr(obj, attribute)
        if getattr(metadata.type(), JSONCLASS_DECORATED, False):
            if isinstance(metadata, _ListField):
                # List of objects
                value = [to_dict(element) for element in value]
            elif isinstance(metadata, _StringDictField):
                # Dict of objects
                value = {k: to_dict(element) for k, element in value.items()}
            else:
                # Object
                value = to_dict(value)

        # Remap the name, if required, to build the dictionary
        mapped_name = metadata.json_name
        dictionary[mapped_name if mapped_name else attribute] = value

    return dictionary
