from typing import Type

from database.models.comment import Comments
from ...database import SessionLocal
from logger import setup_logger

setup_logger('comments_cruds')


class CommentCRUD:
    def __init__(self):
        self.db = SessionLocal()

    def insert(self, **kwargs) -> None:
        data = Comments(**kwargs)
        self.db.add(data)
        self.db.commit()
        self.db.close()

    def find_one(self, **kwargs) -> Comments | None:
        try:
            query = self.db.query(Comments)
            result = query.filter_by(**kwargs).first()
            return result
        finally:
            self.db.close()
