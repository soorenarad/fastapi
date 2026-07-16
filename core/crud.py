from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def create_user_crud(db: AsyncSession, user: User) -> User:
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=user.password_hash,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_all_users_crud(db: AsyncSession) -> Sequence[User]:
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user_by_id_crud(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email_crud(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def update_name_crud(db: AsyncSession, user_id: int, name: str) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        return None

    user.name = name
    await db.commit()
    await db.refresh(user)

    return user
