from sqlalchemy import String, Column, Integer, DateTime, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "BlogMaster"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('UserMaster.id'))
    title = Column(String(255))
    body = Column(String(5000))
    created_date = Column(DateTime)
    created_by_name = Column(String(255))

    creator = relationship("User", back_populates='blogs')


class User(Base):
    __tablename__ = "UserMaster"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(1000))
    created_date = Column(DateTime)

    blogs = relationship('Blog', back_populates='creator')