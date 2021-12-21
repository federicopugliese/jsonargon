import functools
import typing

from jsonargon.deserializer import from_json, from_dict
from jsonargon.fields.simple import JSONCLASS_DECORATED, Nullable
from jsonargon.serializer import to_json, to_dict


def jsonclass(cls):

    @functools.wraps(cls)
    def _as_json_class():

        # Instantiate the object
        obj = cls()

        # Check class attributes
        annotations = typing.get_type_hints(cls)
        for attribute, metadata in annotations.items():

            # Create the attribute for the object
            setattr(obj, attribute, metadata.type() if not isinstance(metadata, Nullable) else None)

        return obj

    # Mark it as wrapped
    _as_json_class.__wrapped__ = cls
    setattr(cls, JSONCLASS_DECORATED, True)

    # Override methods
    # Representation
    setattr(cls, "__repr__", lambda s: to_json(s).replace("\n", ""))
    # To json/dict and from json/dict as class/object methods
    setattr(cls, "to_json", to_json)
    setattr(_as_json_class, "from_json", lambda string: from_json(string, _as_json_class))
    setattr(cls, "to_dict", to_dict)
    setattr(_as_json_class, "from_dict", lambda dictionary: from_dict(dictionary, _as_json_class))

    return _as_json_class

