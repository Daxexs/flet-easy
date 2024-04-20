from peewee import CharField, Model

from models.connection import db


class User(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([User])
