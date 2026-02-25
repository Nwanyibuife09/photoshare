from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PhotoBase(BaseModel):
    title: str
    caption: str
    location: Optional[str] = None
    tags: Optional[str] = None
    
class PhotoCreate(PhotoBase):
    pass

class PhotoResponse(PhotoBase):
    id: int
    s3_path: str
    thumbnail_path: Optional[str] = None
    created_at: datetime
    owner_id: int
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_creator: bool
    
    class Config:
        from_attributes = True
