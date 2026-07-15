from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import User

from collections.abc import Sequence


async def create_user_crud(
    db: AsyncSession,
    user: User
):
    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user

async def get_all_users_crud(db: AsyncSession) -> Sequence[User]:
    result = await db.execute(select(User))
    users = result.scalars().all()

    return users

async def get_user_by_id(
    db: AsyncSession,
    user_id: int
) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    return user

async def get_user_by_email(
    db: AsyncSession,
    email: str
) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )

    return result.scalar_one_or_none()
