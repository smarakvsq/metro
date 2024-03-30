from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import threading

conn_string = "postgresql+asyncpg://metro:Metro2024@13.233.101.243:5432/metro"
# conn_string = "postgresql+asyncpg://vms_user:1234@localhost:5432/metro"

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
