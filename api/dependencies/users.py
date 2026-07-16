from fastapi import Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import create_access_token, hash_password, verify_password
from api.schemas import UserCreate
from core.crud import create_user_crud, get_user_by_id_crud
from core.db import get_db
from core.models import User


async def get_existing_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await get_user_by_id_crud(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def register_user(user_data: UserCreate, db: AsyncSession) -> User:
    password = await run_in_threadpool(hash_password, user_data.password)

    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=password,
    )

    return await create_user_crud(db, user)


async def verify_user(user: User, password: str) -> str | None:
    is_correct = await run_in_threadpool(verify_password, password, user.password_hash)

    if is_correct:
        return create_access_token(user)

    return None
