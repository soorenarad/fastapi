from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from core.config import settings



engine = create_async_engine(
    settings.database_url,
    connect_args={
        "check_same_thread": False
    },
    echo=True,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session