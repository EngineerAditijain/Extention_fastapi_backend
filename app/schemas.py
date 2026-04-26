from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


# =========================
# 🔐 AUTH SCHEMAS
# =========================

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# 🤖 AI / CHAT SCHEMAS
# =========================

class ChatCreate(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    id: int
    prompt: str
    response: str
    created_at: datetime

    class Config:
        from_attributes = True