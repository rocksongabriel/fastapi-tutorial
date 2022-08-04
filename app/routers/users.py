from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import schemas, utils, models
from app.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user object and return it"""

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    try:
        db.add(new_user)
        db.commit()
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {user.email} already exists",
        )
    else:
        db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserRead)
def get_user(id: int, db: Session = Depends(get_db)):
    """Get user data from the database by id"""
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=f"User with id {id} does not exist",
        )

    return user
