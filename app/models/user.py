from sqlalchemy import Boolean, Column, Date, Integer, String, select
from datetime import datetime
from uuid import uuid4
from app.db import Base, get_session
from app.metro_logging import app_logger as logger


def get_uuid():
    return uuid4().hex


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, default=get_uuid())
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date, default=datetime.utcnow())
    updated_at = Column(Date)

    @classmethod
    async def create(cls, username, email, password_hash):
        user: User = cls(username=username, email=email, password_hash=password_hash)
        logger.debug(f"Creating user: {username}.")
        async with get_session() as s:
            s.add(user)
            try:
                await s.commit()
            except Exception as exc:
                logger.error(f"Failed to create user. {exc}")
                await s.rollback()
                return None
        return user
    
    @classmethod
    async def get_by_id(cls, user_id):
        logger.debug(f"Fetching user with id: {user_id}")
        async with get_session() as s:
            result = await s.execute(select(cls).where(cls.id == user_id))
            return result.scalars().first()

    @classmethod
    async def get_by_username(cls, username):
        logger.debug(f"Fetching user with username: {username}")
        async with get_session() as s:
            result = await s.execute(select(cls).where(cls.username == username))
            return result.scalars().first()

    @classmethod
    async def get_by_email(cls, email):
        logger.debug(f"Fetching user with email: {email}")
        async with get_session() as s:
            result = await s.execute(select(cls).where(cls.email == email))
            return result.scalars().first()

    async def update(self, **kwargs):
        logger.debug(f"Update user with values {kwargs}")
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        async with get_session() as s:
            s.add(self)
            await s.commit()

    async def delete(self):
        logger.debug(f"Delete user {self.username}")
        async with get_session() as s:
            await s.delete(self)
            await s.commit()

