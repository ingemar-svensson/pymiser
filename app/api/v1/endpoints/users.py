# app/api/v1/endpoints/users.py

from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.services.user_service import create_user
from app.core.security import get_current_user

router = APIRouter()

@router.post("/users/", response_model=UserOut)
async def register_user(user: UserCreate):
    new_user = await create_user(user)
    return new_user

@router.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserOut(username=current_user.username, email=current_user.email)
