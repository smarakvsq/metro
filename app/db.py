from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


conn_string = "postgresql+asyncpg://vms_user:1234@localhost:5432/metro"

Base = declarative_base()

engine = create_async_engine(
    conn_string,
    echo=True,
    future=True,
)


def async_session_generator():
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )
    return async_session


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
