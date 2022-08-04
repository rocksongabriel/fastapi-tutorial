from jose import jwt, JWTError
from datetime import datetime, timedelta


ALGORITHM = "HS256"
SECRET_KEY = "tq22@u2fday)k4y8%1*rx*!&5769^r"
TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    """Take data and encode it into a jwt token."""

    data_to_encode = data.copy()
    expiration_time = datetime.now() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": str(expiration_time)})
    access_token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return access_token
