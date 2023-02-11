from fastapi import APIRouter, status, Depends, HTTPException, UploadFile
from ..schemas import Login
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
from ..schemas import ShowUser 
from ..hash import Hash

router = APIRouter(
    tags=["Auth"],
    prefix="/auth"
)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=ShowUser)
def login(credentials : Login, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    # if not Hash.verify(credentials.password, user.password):
    #     return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    #! Generate a JWT and return
    return user