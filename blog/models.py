from sqlalchemy import String, Column, Integer
from .database import Base


class Blog(Base):
    __tablename__ = "BlogMaster"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)