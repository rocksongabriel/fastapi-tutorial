from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, ForeignKey


class Post(Base):
    """Database model for posts table"""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="posts")


class User(Base):
    """SQLAlchemy Database model for a user"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    posts = relationship("Post", back_populates="owner")
