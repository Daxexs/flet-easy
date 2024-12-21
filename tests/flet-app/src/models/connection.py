from pathlib import Path

from tortoise import Tortoise

path = Path(__file__).parents[1] / "assets"


async def db_init():
    """connect to the database"""
    await Tortoise.init(
        db_url=f"sqlite://{path}/database.db",
        modules={"models": ["models.models"]},
    )
    await Tortoise.generate_schemas()


async def db_close():
    """close the database"""
    await Tortoise.close_connections()
