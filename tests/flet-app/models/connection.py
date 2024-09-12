from pathlib import Path

from peewee import SqliteDatabase

path = Path(__file__).parent.parent / "assets"

db = SqliteDatabase(path / "database.db")
