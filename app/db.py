import threading
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import Settings

settings = Settings()

conn_string = f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"

print(f"Connection string: {conn_string}")

Base = declarative_base()
db_connections = threading.local()


def get_sessionmaker():
    if not hasattr(db_connections, "engine"):
        db_connections.engine = create_async_engine(conn_string, pool_size=1000, echo=True)
    if not hasattr(db_connections, "sessionmaker"):
        db_connections.sessionmaker = sessionmaker(
            bind=db_connections.engine, autoflush=False, class_=AsyncSession
        )
    return db_connections.sessionmaker


@asynccontextmanager
async def get_session():
    try:
        async with get_sessionmaker()() as session:
            yield session
    except:
        await session.rollback()
    finally:
        await session.close()
