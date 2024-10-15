# app/models/user.py

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: Optional[str] = Field(alias="_id")
    username: str
    email: EmailStr
    hashed_password: Optional[str] = None
    oauth_providers: List[str] = []
