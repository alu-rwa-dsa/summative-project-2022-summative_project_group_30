from datetime import datetime as dt
from mongoengine import *


class User(Document):
    username = StringField(required=True, max_length=30, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    password = StringField(required=True)
    email_address = EmailField(required=True, unique=True)
    timestamp = DateTimeField(default=dt.now())
    meta = {
        'auto-create-index': True,
        'db_alias': 'busSystem',
        'allow_inheritance': True
    }


class Bus(Document):
    departure_period = StringField()
    last_check_time = DateTimeField(default=dt.now())
    name = StringField(unique=True)
    capacity = IntField()
    passengers = ListField()
    meta = {
        'auto-create-index': True,
        'db_alias': 'busSystem',
        'allow_inheritance': True
    }

