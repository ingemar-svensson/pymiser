# app/services/user_service.py

from app.models.user import User
from app.schemas.user import UserCreate
from app.db.database import get_user_collection
from app.utils.hashing import get_password_hash, verify_password
from app.core.config import settings
from fastapi import HTTPException, status

async def create_user(user: UserCreate) -> User:
    user_collection = get_user_collection()
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(user.password)
    user_dict = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "oauth_providers": []
    }
    await user_collection.insert_one(user_dict)
    return User(**user_dict)

async def authenticate_user(username: str, password: str) -> User | None:
    user_collection = get_user_collection()
    user_data = await user_collection.find_one({"username": username})
    if user_data and verify_password(password, user_data.get('hashed_password', '')):
        return User(**user_data)
    return None

async def get_user_by_username(username: str) -> User | None:
    user_collection = get_user_collection()
    user_data = await user_collection.find_one({"username": username})
    if user_data:
        return User(**user_data)
    return None

async def create_or_get_user(user_info: dict, provider: str) -> User:
    user_collection = get_user_collection()
    email = user_info['email']
    user_data = await user_collection.find_one({"email": email})
    if not user_data:
        # Create new user
        username = email.split('@')[0]
        user_dict = {
            "username": username,
            "email": email,
            "oauth_providers": [provider]
        }
        await user_collection.insert_one(user_dict)
        return User(**user_dict)
    else:
        # Update oauth_providers
        if provider not in user_data.get('oauth_providers', []):
            user_data['oauth_providers'].append(provider)
            await user_collection.update_one(
                {"_id": user_data["_id"]},
                {"$set": {"oauth_providers": user_data['oauth_providers']}}
            )
        return User(**user_data)
