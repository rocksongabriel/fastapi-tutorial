from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, utils, oauth2


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Take user `attempted` login credentials and return a token if login
    is successful
    """

    user = (
        db.query(models.User)
        .filter(models.User.email == credentials.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_NOT_FOUND, detail="Invalid Credentials"
        )

    verified = utils.verify_password(credentials.password, user.password)

    if not verified:
        raise HTTPException(
            status_code=status.HTTP_403_NOT_FOUND, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(
        {"user_id": user.id, "created": str(user.created)}
    )

    return {"acces_token": access_token, "token_type": "Bearer"}
