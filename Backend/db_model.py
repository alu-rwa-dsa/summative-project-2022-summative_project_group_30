from datetime import datetime as dt
from mongoengine import *

from configs.db_conn import connect_db


try:
    connect_db('busSystemDSA')
except Exception as e:
    print(e)


class User(Document):
    username = StringField(required=True, max_length=30, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    password = StringField(required=True)
    email_address = EmailField(required=True, unique=True)
    timestamp = DateTimeField(default=dt.now())
    meta = {
        'auto-create-index': True,
        'alias': 'bus-system',
        'allow_inheritance': True
    }


class Bus(Document):
    departure_period = StringField()
    last_check_time = DateTimeField(default=dt.now())
    name = StringField(unique=True)
    capacity = IntField()
    passengers = ListField()
