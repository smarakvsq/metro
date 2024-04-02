from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Base(BaseSettings):
    env_name: str = Field(..., env="ENV")
    # env_name: str = os.environ.get("ENV", "dev")

    class Config:
        case_sensitive = False
        env_file = "./.env"


class Dev(Base):
    env_name: str
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")
    db_host: str = Field(..., env="DB_HOST")
    db_name: str = Field(..., env="DB_NAME")

    class Config:
        env_file = "./dev.env"


class Test(Base):
    env_name: str
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")
    db_host: str = Field(..., env="DB_HOST")
    db_name: str = Field(..., env="DB_NAME")

    class Config:
        env_file = "./test.env"


class Client(Base):
    env_name: str
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")
    db_host: str = Field(..., env="DB_HOST")
    db_name: str = Field(..., env="DB_NAME")

    class Config:
        env_file = "./client.env"


base_settings = Base()
mapper = {"dev": Dev, "test": Test, "client": Client}
Settings = mapper.get(base_settings.env_name, "dev")
# sett = Settings()
# print(f"postgresql+asyncpg://{sett.db_user}:{sett.db_pass}@{sett.db_host}/{sett.db_name}")
