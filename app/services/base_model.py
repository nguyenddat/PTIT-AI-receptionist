import json
from fastapi import WebSocket
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from database.database import Base

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_response(self, response: dict, websocket: WebSocket):
        message = json.dumps(response)
        await websocket.send_text(message)

    async def broadcast(self, response: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(response))
            
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


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)