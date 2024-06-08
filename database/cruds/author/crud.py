from typing import Type

from database.models.author import Authors
from ...database import SessionLocal
from logger import setup_logger

setup_logger('author_cruds')


class AuthorCRUD:
    def __init__(self):
        self.db = SessionLocal()

    def insert(self, **kwargs) -> None:
        data = Authors(**kwargs)
        self.db.add(data)
        self.db.commit()
        self.db.close()

    def find_one(self, **kwargs) -> Type[Authors] | None:
        try:
            query = self.db.query(Authors)
            result = query.filter_by(**kwargs).first()
            return result
        finally:
            self.db.close()
