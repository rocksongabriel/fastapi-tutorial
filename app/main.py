from fastapi import FastAPI
from .database import engine
from . import models
from app.routers import posts, users, auth


# Create the database tables
models.Base.metadata.create_all(bind=engine)


# Initialize app
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def home():
    """The base endpoint"""

    return "Home of Tutorial"
