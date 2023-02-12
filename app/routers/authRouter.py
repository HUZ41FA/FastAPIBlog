from fastapi import APIRouter, status, Depends, HTTPException
from ..schemas import Login, LoginUser
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
from ..schemas import ShowUser 
from ..hash import Hash
from datetime import timedelta
from ..token import ACCESS_TOKEN_EXPIRY_MINUTES, create_access_token

router = APIRouter(
    tags=["Auth"],
    prefix="/auth"
)


@router.post('/login', status_code=status.HTTP_200_OK)
def login(credentials : Login, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not Hash.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"username":user.username, "email":user.email, "access_token":access_token, "token_type":"bearer"}

