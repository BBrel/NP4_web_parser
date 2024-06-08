from sqlalchemy import Column, String, INT
from ..database import Base


class Authors(Base):
    __tablename__ = "authors"
    id = Column(INT, primary_key=True)
    name = Column(String)
