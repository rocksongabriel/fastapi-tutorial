import time
from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


# Initialize app
app = FastAPI()


# Make connection to postgres database
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="myFastAPIDatabase",
            user="darkbotbbl",
            password="testpass1234",
            cursor_factory=RealDictCursor,
        )
    except psycopg2.OperationalError as error:
        print("Connecting to database failed")
        print(f"Error: {error}")
        time.sleep(2)
    else:
        cursor = conn.cursor()
        print("Database connection established successfully")
        break


# Schemas
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
def home():
    """The base endpoint"""
    return "Home of Tutorial"


@app.get("/posts")
async def all_posts(db: Session = Depends(get_db)):
    """Return all posts"""
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{post_id}")
async def get_post(post_id: int, db: Session = Depends(get_db)):
    """Find a post of id `post_id` and return it"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    return {"data": post}


@app.post("/posts")
async def create_post(post: Post, db: Session = Depends(get_db)):
    """Add a new post to the database and return it"""
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


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


@app.put("/posts/{post_id}")
def update_post(
    post_id: int,
    updated_post: Post,
    db: Session = Depends(get_db)
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

    return {"detail": post_query.first()}
