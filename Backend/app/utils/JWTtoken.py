from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from jose import jwt,JWTError
from app.core.responce import ApiResponse,ApiError

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verifyJWT(token : str):
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract user identity (we usually store email or user_id in "sub")
        user_identity: str = payload.get("sub")

        if user_identity is None:
            raise ApiError(message="Unothorized access",status_code=401) 

        return user_identity  # valid token ✅

    except JWTError:
        raise ApiError(message="Unothorized access",status_code=401,errors=JWTError) 