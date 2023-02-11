from typing import List
from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import ShowUser, User
from datetime import datetime
from ..hash import Hash
from ..repository import userRepository 

router = APIRouter(
    tags=['User'],
    prefix='/user'
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create_user(user : User, db : Session = Depends(get_db)):
    user.password = Hash.hash_bcrypt(user.password)
    new_user = models.User(username = user.username, email = user.email, password = user.password, created_date = datetime.now())

    userRepository.create_user(new_user, db)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
async def get_user(id: int, db : Session = Depends(get_db)):
    user = userRepository.get_by_id(id, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} not found")
    return user
