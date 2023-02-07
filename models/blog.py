from sqlalchemy import String, Column, Integer, DateTime
from services.database.database_service import Base


class Blog(Base):
    __tablename__ = "BlogMaster"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    body = Column(String(5000))
    created_date = Column(DateTime)
    created_by_name = Column(String(255))