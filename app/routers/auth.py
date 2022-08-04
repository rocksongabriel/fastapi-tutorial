from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, utils, oauth2


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).\
            filter(models.User.email == credentials.email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

    verified = utils.verify_password(credentials.password, user.password)

    if not verified:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(
        {"user_id": user.id, "created": str(user.created)}
    )

    return {"acces_token": access_token, "token_type": "Bearer"}
