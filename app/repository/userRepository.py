from typing import List
from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import Blog, ShowBlog, ShowUser, User
from datetime import datetime
from ..hash import Hash


def get_by_id(id : int, db : Session) -> List[models.User]:
    return db.query(models.User).filter(models.User.id == id).first()


def create_user(model : models.User, db : Session):
    db.add(model)
    return True