from peewee import DoesNotExist, IntegrityError

from models.models import User, db


def add_user(user: User):
    try:
        with db.atomic():
            User.create(username=user.username, password=user.password)
            return True
    except IntegrityError:
        return False


def check_user(user: User):
    try:
        user_check = User.get(User.username == user.username)
        return user_check.password == user.password
    except DoesNotExist:
        return False


def delete_user(user: User):
    try:
        with db.atomic():
            User.get(username=user.username).delete_instance()
            return True
    except IntegrityError:
        return False
