from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.routers.products import router as products_router
from api.routers.users import router as users_router

from core.db import engine
from core.models import Base


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    await create_tables()

    yield

    # Shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def my_middleware(request: Request, call_next):
    print('received request')

    response = await call_next(request)

    print("Response sent")

    return response


app.include_router(products_router)
app.include_router(users_router)

