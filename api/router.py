from fastapi import APIRouter

from api.routers.products import router as products_router
from api.routers.users import router as users_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(users_router)
api_router.include_router(products_router)
