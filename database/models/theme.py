from sqlalchemy import Column, String, INT
from ..database import Base


class Theme(Base):
    __tablename__ = "themes"
    id = Column(INT, primary_key=True)
    name = Column(String)
