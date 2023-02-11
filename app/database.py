from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:NewPassword@127.0.0.1:3306/blog"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
