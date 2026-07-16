from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


class UserUpdateName(BaseModel):
    name: str


class UserResponseLogin(BaseModel):
    id: int
    name: str
    email: str
    access_token: str
    token_type: str = "bearer"


class ProtectedProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    message: str
