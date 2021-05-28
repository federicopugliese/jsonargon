JSONCLASS_DECORATED = "__jsonclass_decorated"


# INTERNAL
class _JsonField:

    def __init__(self, type, json_name=None):
        self.type = type
        self.json_name = json_name


# PUBLIC
class Nullable(_JsonField):
    pass


class Required(_JsonField):
    pass
