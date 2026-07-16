from fastapi import APIRouter, Depends, HTTPException

from api.deps import CurrentUser, DbSession
from api.dependencies.users import get_existing_user, register_user, verify_user
from core.models import User
from api.schemas import (
    ProtectedProfileResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserResponseLogin,
    UserUpdateName,
)
from core.crud import get_all_users_crud, get_user_by_email_crud, update_name_crud

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=ProtectedProfileResponse)
async def get_current_user_profile(current_user: CurrentUser) -> ProtectedProfileResponse:
    return ProtectedProfileResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        message="Authenticated profile retrieved successfully",
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: DbSession) -> UserResponse:
    user = await get_user_by_id_crud(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: DbSession) -> list[UserResponse]:
    users = await get_all_users_crud(db)

    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    return list(users)


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: DbSession) -> UserResponse:
    existing_user = await get_user_by_email_crud(db, user.email)

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    created_user = await register_user(user, db)
    return created_user


@router.patch("/{user_id}/name", response_model=UserResponse)
async def update_name(
    payload: UserUpdateName,
    db: DbSession,
    user: User = Depends(get_existing_user),
) -> UserResponse:
    updated_user = await update_name_crud(db, user.id, payload.name)
    return updated_user


@router.post("/login", response_model=UserResponseLogin)
async def login(payload: UserLogin, db: DbSession) -> UserResponseLogin:
    existing_user = await get_user_by_email_crud(db, payload.email)

    if not existing_user:
        raise HTTPException(status_code=409, detail="User doesn't exists")

    token = await verify_user(existing_user, payload.password)

    if not token:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return UserResponseLogin(
        id=existing_user.id,
        name=existing_user.name,
        email=existing_user.email,
        access_token=token,
    )
