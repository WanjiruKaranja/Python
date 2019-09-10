from peewee import *
from os import path
ROOT = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(ROOT,"users.db"))

class User(Model):
    names = CharField()
    email = CharField(unique=True)
    password = CharField()
    class Meta:
        database = db


class Posts(Model):
    names = CharField()
    place = CharField()
    date = CharField()
    time = CharField()
    cost = DecimalField()
    content = CharField()

    class Meta:
        database = db


User.create_table(fail_silently=True)
Posts.create_table(fail_silently=True)
