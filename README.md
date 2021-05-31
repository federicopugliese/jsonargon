# JSON Argon

https://gitlab.com/federico_pugliese/jsonargon

**Serialization** and **deserialization** of **JSON** objects from/into **Python** objects (with **validation** and **remapping** capabilities).

The underlying idea is to **annotate** a Python **Class** with metadata useful to serialize its objects into JSON strings and viceversa.

Main features and goals are:

- Concision
- JSON Validation
- Optional remapping of fields name
- Familiar interface

## Installation

To get the latest stable version, just run

```
pip install jsonargon
```

or

```
pip install jsonargon==<version>
```

if you require a specific version.

## Usage

### Basic Usage

The basic requirement is to write the Python Class remapping your JSON.

```
from jsonargon.decorators import jsonclass
from jsonargon.fields.simple import Required, Nullable

@jsonclass
class Person:
    
    name: Required(str)
    age:  Nullable(int)
    
```

As simple as that. The `name` field is a required string, while the `age` is a non-required integer.

The `Required` type annotation will make sure that `name` is in your JSON string before deserializing it (a `KeyError` is thrown otherwise).

If you have your JSON string, you can easily remap it into a Python object of that class, after you get your JSON string somehow (probably something like `{"name": "Jason Argonaut"}`):
```
person = Person.from_json(your_json_string)
```
```
print(person.name)  # Jason Argonaut
print(person.age)   # None
```

You can also serialize your object into a JSON string.

```
person_json_string = person.to_json()
```

### Advanced usage

JSON Argon also supports:

- Nested objects
- Lists and Dictionaries
- JSON-Python names remapping

#### Fields

Each field annotation support these parameters:

```
<field>(type: Any, json_name: str = None)
```

- `type` is a simple type like `str`, `int`, `float` or a Class
- `json_name` is an *optional* string representing the corresponding name in JSON


| Field  | Meaning | JSON |
|---|---|---|
| `Required` | A required, simple attribute  | `"name": "Jason"`  |
| `Nullable`  | A nullable (`None`) simple attribute | As above, or `"name": null` or no attribute at all |
| `RequiredList`  | A required (but maybe empty) list of objects of the specified `type` | `"names": ["Argo", "Atalanta"]`, or `"names": []` or `"crew": [{"name": "Argo"}, {"name": "Atalanta"}]` |
| `NullableList`  | A nullable list of objects of the specified `type` | As above, or `"names": null` or no attribute at all |
| `RequiredStringDict`  | A required (but maybe empty) dict of string -> objects of the specified `type` | `"tags": {"scope": "dev"}`, or `"tags": {}` or `"documents": {"name": {"length":12}}` |
| `NullableStringDict`  | A required (but maybe empty) list of objects of the specified `type` | As above, or `"tags": null` or no attribute at all |

You can find a complete example here (with the JSON below):

```
from jsonargon.decorators import jsonclass
from jsonargon.fields.simple import Required, Nullable
from jsonargon.fields.dict import RequiredStringDict
from jsonargon.fields.list import RequiredList

@jsonclass
class Size:
    
    length: Required(float)
    width:  Required(float)
    height: Nullable(float, "heigth")  # Correct a JSON typo


@jsonclass
class Member:

    name: Required(str)
    role: Nullable(str)
    

@jsonclass
class Ship:
    
    name: Required(str, "shipName")
    size: Required(Size)
    crew: RequiredList(Member, "members")
    attributes: RequiredStringDict(str)

```

To remap:
```
{
    "shipName": "Argo",
    "size": {
        "width": 45.4,
        "length": 34.2
    },
    "members": [
        {
            "name": "Atalanta"
        },
        {   
            "name": "Jason",
            "role": "leader"
        }
    ]
    "attributes": {
        "rarity": "mythological",
        "status": "destroyed"
    }
}

```


## Origin of the name

There are several reasons behind the name of this library.

First of all, in Greek mythology, Jason was the leader of Argonauts.

Jason is quite similar to JSON pronunciation. He was the hero who defeated the monstrous dragon (often depicted as a giant snake - a clear reference to Python) that guarded the Golden Fleece. 

Also, his ship was Argo, and the Argonauts his crew.

Argon, instead, is a noble gas. And with the same Class and style of a noble, this library aims to make you write a much cleaner code when dealing with JSON.

*Make Jason proud of your code and join his crew of Argonauts.*
