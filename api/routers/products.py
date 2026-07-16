from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
async def get_products(category: str, limit: int = 10) -> dict[str, str | int]:
    return {
        "category": category,
        "limit": limit,
    }
