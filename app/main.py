from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Any, Iterable, Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


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
    rating: Optional[int] = None
    published: bool = True


@app.get("/")
def home():
    """The base endpoint"""
    return "Home of Tutorial"


@app.get("/posts")
async def all_posts():
    """Return all posts"""
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    """Find a post of id `post_id` and return it"""
    cursor.execute(
        """
        SELECT * FROM posts p WHERE p.id = %s
        """,
        str(post_id),
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} was not found",
        )
    return {"data": post}


@app.post("/posts")
async def create_post(post: Post):
    """Add a new post to the database and return it"""
    cursor.execute(
        """
        INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    conn.commit()
    new_post = cursor.fetchone()
    return {"data": new_post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    """Delete a post from the database"""
    cursor.execute(
        """
        DELETE FROM posts p WHERE p.id = %s RETURNING *
        """,
        str(post_id),
    )
    conn.commit()
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Post with id {post_id} does not exist",
        )


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    """Update a given post by id in the database and return it"""
    cursor.execute(
        """
        UPDATE posts p SET title = %s, content = %s, published = %s WHERE p.id = %s RETURNING *
        """,
        (post.title, post.content, post.published, str(post_id)),
    )
    conn.commit()
    updated_post = cursor.fetchone()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist",
        )

    return {"detail": updated_post}
