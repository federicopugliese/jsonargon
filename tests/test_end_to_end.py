import json

from jsonargon.decorators import jsonclass
from jsonargon.fields.dict import RequiredStringDict
from jsonargon.fields.list import RequiredList
from jsonargon.fields.simple import Required, Nullable


@jsonclass
class Address:

    street: Required(str, "AddressStreet")
    code: Nullable(str)
    aliases: RequiredStringDict(int)


@jsonclass
class Phone:

    prefix: Required(str)
    number: Required(str)
    country: Nullable(str)


@jsonclass
class Customer:

    name: Required(str, "Name")
    address: Nullable(Address)
    mails: RequiredList(str)
    phones: RequiredList(Phone, "PhoneNumbers")


def test_serialization():

    # Prepare objects
    # Address
    address = Address()
    address.street = "A street"
    address.aliases = {"ok": 1}
    # Phone
    phone = Phone()
    phone.prefix = "+39"
    phone.number = "35878935315135"
    # Customer
    customer = Customer()
    customer.name = "A name"
    customer.address = address
    customer.mails = []
    customer.phones = [phone]

    # To json
    customer_json = customer.to_json()

    # Test it
    customer_dict = json.loads(customer_json)
    assert customer_dict == {
        "Name": "A name",
        "address": {
            "AddressStreet": "A street",
            "aliases": {
                "ok": 1
            },
            "code": None
        },
        "mails": [],
        "PhoneNumbers": [
            {
                "prefix": "+39",
                "number": "35878935315135",
                "country": None
            }
        ]
    }


def test_deserialization():

    # Prepare json
    customer_dict = {
        "Name": "thisname",
        "address": {
            "AddressStreet": "thisstreet",
            "aliases": {
                "ok": 1
            },
            "code": None
        },
        "mails": [],
        "PhoneNumbers": [
            {
                "prefix": "+39",
                "number": "35878935315135",
                "country": None
            }
        ]
    }
    customer_json = json.dumps(customer_dict)

    # Load json to objects
    customer = Customer.from_json(customer_json)

    # Test it
    assert (
            customer.name == "thisname" and
            customer.address.street == "thisstreet" and
            customer.address.aliases["ok"] == 1 and
            customer.mails == [] and
            customer.phones[0].prefix == "+39"
    )
