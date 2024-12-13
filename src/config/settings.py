from os import getenv
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class DB(BaseSettings):
    DB_URL = getenv("DB_URL")


class Settings(BaseSettings):
    DEBUG: bool = True
    SECRET_KEY: str = getenv("SECRET_KEY")
    HOST: str = getenv("HOST", "127.0.0.1")
    PORT: int = getenv("PORT", 8000)

    DB: DB = DB()
