import datetime as datetime
from email.policy import default
from sqlalchemy import Column, ForeignKey, Integer, Boolean, String, DateTime
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt

from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    group = Column (String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    is_active = Column(Boolean, default=True)
    posts = relationship("Post", back_populates="user")

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    user = relationship("User", back_populates="posts")