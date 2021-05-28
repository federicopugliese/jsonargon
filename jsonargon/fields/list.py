from jsonargon.fields.simple import Nullable, Required, _JsonField


# INTERNAL
class _ListField(_JsonField):
    pass


# PUBLIC
class RequiredList(Required, _ListField):
    pass


class NullableList(Nullable, _ListField):
    pass
