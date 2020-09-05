from peewee import *
import datetime
import os
from flask_login import UserMixin
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('dogs.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(unique=True)
    name = CharField()
    photo_url = CharField()
    location = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class Car(Model):
    name = CharField()
    make = CharField()
    model = CharField()
    year = CharField()
    photo_url = CharField()
    votes = IntegerField(default=0)
    builder = ForeignKeyField(User, backref='cars')

    class Meta:
        database = DATABASE


class Project(Model):
    title = CharField()
    date_begin = DateField(default=datetime.datetime.now)
    date_end = DateField(default=datetime.datetime.now)
    details = TextField()
    photo_url = CharField()
    car = ForeignKeyField(Car, backref='projects')

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Car, Project], safe=True)
    print("Tables created")
    DATABASE.close()
