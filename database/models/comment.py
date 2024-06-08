from sqlalchemy import Column, String, ForeignKey, INT
from ..database import Base


class Comments(Base):
    __tablename__ = "comments"
    id = Column(INT, primary_key=True)
    theme_id = Column(INT, ForeignKey("themes.id"), nullable=False)
    author_id = Column(INT, nullable=False)
    quote_id = Column(INT)
    comment_text = Column(String)
