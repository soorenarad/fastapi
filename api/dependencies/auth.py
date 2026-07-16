import hashlib
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.crud import get_user_by_email_crud
from core.db import get_db
from core.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


def hash_password(password: str) -> str:
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.hash(password_hash)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return pwd_context.verify(password_hash, hashed_password)


def create_access_token(user: User) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": user.email,
        "exp": expire,
    }

    return jwt.encode(payload, settings.secret_key, settings.algorithm)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        user_email = payload.get("sub")

        if user_email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await get_user_by_email_crud(db, user_email)

    if user is None:
        raise credentials_exception

    return user
