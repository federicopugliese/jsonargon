import json
import typing
from typing import Type

from jsonargon.fields.dict import _StringDictField
from jsonargon.fields.list import _ListField
from jsonargon.fields.simple import JSONCLASS_DECORATED, Nullable

T = typing.TypeVar('T')


def from_json(string: str, cls: Type[T]) -> T:

    # String -> dictionary
    dictionary = json.loads(string)

    # From dictionary to class
    return from_dict(dictionary, cls)


def from_dict(dictionary: dict, cls: Type[T]) -> T:

    obj = cls()

    # Inspect the class
    annotations = typing.get_type_hints(cls)
    for attribute, metadata in annotations.items():

        # Remap the name, if required, to build the object
        mapped_name = metadata.json_name if metadata.json_name else attribute

        # Get the value of that attribute (if it's a nested serializable class, do this recursively)
        value = dictionary[mapped_name] if not isinstance(metadata, Nullable) else dictionary.get(mapped_name)
        if getattr(metadata.type(), JSONCLASS_DECORATED, False):
            if isinstance(metadata, _ListField):
                # List of objects
                value = [from_dict(element, metadata.type) for element in value]
            elif isinstance(metadata, _StringDictField):
                # Dict of objects
                value = {k: from_dict(element, metadata.type) for k, element in value.items()}
            else:
                # Object
                value = from_dict(value, metadata.type)

        # Set it for the object
        setattr(obj, attribute, value)

    return obj

