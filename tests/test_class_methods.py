import json

from jsonargon.decorators import jsonclass
from jsonargon.fields.simple import Required, Nullable


@jsonclass
class Person:

    name: Required(str)
    age: Nullable(int)


def test_to_json():

    person = Person()
    person.name = "Jason"
    person_json = person.to_json()
    assert json.loads(person_json)["name"] == "Jason"


def test_from_json():

    person = Person.from_json('{"name": "Jason"}')
    assert person.name == "Jason"


def test_to_json_from_json():

    person = Person.from_json('{"name": "Jason"}')
    person_json = person.to_json()
    assert json.loads(person_json)["name"] == "Jason"
