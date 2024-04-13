
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from .env import CNN_URI
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = CNN_URI or ""
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
def db_startup():
    # SQLModel.metadata.create_all(engine)
    pass
SessionLocal  = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False,
    autocommit = False,
    autoflush = False,
)
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session