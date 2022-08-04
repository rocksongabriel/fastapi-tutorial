from jose import jwt, JWTError
from datetime import datetime, timedelta
from app import schemas
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer("login")


ALGORITHM = "HS256"
SECRET_KEY = "tq22@u2fday)k4y8%1*rx*!&5769^r"
TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    """Take data and encode it into a jwt token."""

    data_to_encode = data.copy()
    expiration_time = datetime.utcnow() + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )
    data_to_encode.update({"exp": str(expiration_time)})
    access_token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return access_token


def verify_access_token(token: str, credentials_exception):
    """Verify the token passed into the function"""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise credentials_exception
    else:
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current authenticated user"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials or non existent account",
    )

    return verify_access_token(token, credentials_exception)
