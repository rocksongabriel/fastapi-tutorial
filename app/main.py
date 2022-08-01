from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Any, Iterable, Optional
from random import randrange


# Initialize app
app = FastAPI()


# Schemas
class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: bool = True


# Data
posts: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "Post One",
        "content": "This is the first post",
        "rating": 4,
        "published": False,
    },
    {
        "id": 2,
        "title": "Post Two",
        "content": "This is the second post",
        "rating": None,
        "published": True,
    },
]


# Find post
def find_post(post_id: int):
    """Filter the posts array and return the post with id post_id"""
    filtered_posts_iterable: Iterable = filter(
        lambda post: post["id"] == post_id, posts
    )
    filtered_posts: list = list(filtered_posts_iterable)
    return filtered_posts[0] if filtered_posts else None


@app.get("/")
def home():
    """The base endpoint"""
    return "Home of Tutorial"


@app.get("/posts")
async def all_posts():
    """Return all posts"""
    return posts


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    """Filter posts for post of id {id} and return the post"""
    post = find_post(post_id)
    if not post:
        msg = {"detail": {"post": f"Post with id {post_id} does not exist"}}
        raise HTTPException(status.HTTP_404_NOT_FOUND, msg)
    return {"detail": {"post": post}}


@app.post("/posts")
async def create_post(post: Post):
    """Add a post to the posts and return the post"""
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    posts.append(post_dict)
    return {"data": post_dict}


def find_post_index(post_id: int) -> Any:
    """Return the index of the post with the given `post_id`"""
    for idx, post in enumerate(posts):
        if post["id"] == post_id:
            return idx


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    """Find and delete post with id `post_id`"""
    post_index: int = find_post_index(post_id)
    if post_index:
        posts.pop(post_index)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"No post with id: {post_id}"},
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    """Find and update post with id `post_id`"""
    post_index: int = find_post_index(post_id)

    if post_index:
        post_dict = post.dict()
        post_dict["id"] = post_id
        posts[post_index] = post_dict
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"No post with id: {post_id}"},
        )
    return {"data": post_dict}
