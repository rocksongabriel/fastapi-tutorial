from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from .database import engine, get_db
from . import models, schemas, utils
from sqlalchemy.orm import Session


# Create the database tables
models.Base.metadata.create_all(bind=engine)


# Initialize app
app = FastAPI()


@app.get("/")
def home():
    """The base endpoint"""

    return "Home of Tutorial"


@app.get("/posts", response_model=List[schemas.Post])
async def all_posts(db: Session = Depends(get_db)):
    """Return all posts"""

    posts = db.query(models.Post).all()

    return posts


@app.get("/posts/{post_id}", response_model=schemas.Post)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    """Find a post of id `post_id` and return it"""

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist"
        )

    return post


@app.post("/posts", response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Add a new post to the database and return it"""

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Delete a post from the database"""

    post = db.query(models.Post).filter(models.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist",
        )

    post.delete(synchronize_session=False)
    db.commit()


@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(
    post_id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)
):
    """Update a given post by id in the database and return it"""

    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


# User related path operations
@app.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user object and return it"""

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users/{id}", response_model=schemas.UserRead)
def get_user(id: int, db: Session = Depends(get_db)):
    """Get user data from the database by id"""
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=f"User with id {id} does not exist"
        )

    return user
