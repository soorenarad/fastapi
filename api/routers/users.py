from fastapi import HTTPException, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.models import User
from api.schemas import UserCreate, UserResponse
from core.db import get_db

from core.crud import create_user_crud, get_user_by_id, get_all_users_crud, get_user_by_email

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/{user_id}", response_model=UserResponse) # for list response_model=List[UserResponse]
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.get("/", response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users_crud(db)


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = User(name=user.name, email=user.email)

    created_user = await create_user_crud(db, new_user)

    return created_user



