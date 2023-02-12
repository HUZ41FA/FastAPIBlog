from fastapi import status, HTTPException, Depends
from fastapi.security import oauth2, OAuth2PasswordBearer
from .token import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from .schemas import TokenData
from .token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return verify_token(token, credentials_exception)