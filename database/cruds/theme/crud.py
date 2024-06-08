from typing import Type

from database.models.theme import Theme
from ...database import SessionLocal
from logger import setup_logger

setup_logger('theme_cruds')


class ThemeCRUD:
    def __init__(self):
        self.db = SessionLocal()

    def insert(self, **kwargs) -> None:
        data = Theme(**kwargs)
        self.db.add(data)
        self.db.commit()
        self.db.close()

    def find_one(self, **kwargs) -> Theme | None:
        try:
            query = self.db.query(Theme)
            result = query.filter_by(**kwargs).first()
            return result
        finally:
            self.db.close()
