# from tortoise import run_async
from tortoise.exceptions import DoesNotExist, IntegrityError

from models.connection import db_close, db_init
from models.models import User


async def add_user(user: User):
    try:
        await db_init()
        await User.create(username=user.username, password=user.password)
        return True
    except IntegrityError:
        return False
    finally:
        await db_close()


async def check_user(user: User):
    try:
        await db_init()
        user_check = await User.get(username=user.username)
        return user_check.password == user.password
    except DoesNotExist:
        return False
    finally:
        await db_close()


async def delete_user(user: User):
    try:
        await db_init()
        await User.filter(User.username == user.username).delete()
    except IntegrityError:
        return False
    finally:
        await db_close()
