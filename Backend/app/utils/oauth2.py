from fastapi import Depends,HTTPException,status

from fastapi.security import OAuth2PasswordBearer
from . import JWTtoken
from app.database.mongoDb import get_user_collection
from pydantic import BaseModel

class auth_token(BaseModel):
    token:str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/", auto_error=True)

async def get_current_user(token:str=Depends(oauth2_scheme)):
     credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
     
     user_decode=JWTtoken.verifyJWT(token=token)
     print(user_decode)

     if user_decode is None:
          raise credentials_exception
     
     return user_decode