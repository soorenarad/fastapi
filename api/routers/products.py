from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.get("/")
def get_products(category: str, limit: int = 10):
    return {
        "category": category,
        "limit": limit
    }