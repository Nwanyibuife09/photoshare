from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_creator = Column(Boolean, default=False)
    
    photos = relationship("Photo", back_populates="owner")
    comments = relationship("Comment", back_populates="author")
    ratings = relationship("Rating", back_populates="rater")

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    caption = Column(String)
    location = Column(String, nullable=True)
    tags = Column(String, nullable=True) # Storing tags as comma-separated string for simplicity
    s3_path = Column(String, unique=True) # Will store the path to cloud storage
    thumbnail_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="photos")
    comments = relationship("Comment", back_populates="photo")
    ratings = relationship("Rating", back_populates="photo")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    author_id = Column(Integer, ForeignKey("users.id"))
    photo_id = Column(Integer, ForeignKey("photos.id"))
    
    author = relationship("User", back_populates="comments")
    photo = relationship("Photo", back_populates="comments")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer) # e.g. 1 to 5
    
    rater_id = Column(Integer, ForeignKey("users.id"))
    photo_id = Column(Integer, ForeignKey("photos.id"))
    
    rater = relationship("User", back_populates="ratings")
    photo = relationship("Photo", back_populates="ratings")
