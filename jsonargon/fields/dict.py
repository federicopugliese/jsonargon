from jsonargon.fields.simple import Nullable, Required, _JsonField


# INTERNAL
class _StringDictField(_JsonField):
    pass


# PUBLIC
class RequiredStringDict(Required, _StringDictField):
    pass


class NullableStringDict(Nullable, _StringDictField):
    pass
