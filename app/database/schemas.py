from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class EventCreate(BaseModel):
    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: str
    
class EventOut(BaseModel):
    id: int
    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: str
    
    class Config:
        orm_mode = True