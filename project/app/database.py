from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from .env import DATABASE_URL
from sqlalchemy.orm import sessionmaker

# Crea una conección asíncrona con base de datos.
engine = create_async_engine(
    DATABASE_URL,
    echo = True,
    future = True,
    pool_size = 5
)
def db_startup():
    # SQLModel.metadata.create_all(engine)
    pass
# Crea una sesión asíncrona única.
SessionLocal  = sessionmaker(
    bind = engine,
    autocommit = False,
    expire_on_commit = False,
    autoflush = False,
    class_ = AsyncSession,
)
        
async def get_db():
    """Get db: Regresa un generador con la sesión.

    Raises:
        e: Cualquier excepción que se pueda esperar.

    Yields:
        AsyncSession: Sesión de base.
    """
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()