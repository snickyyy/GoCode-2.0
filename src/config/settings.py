from os import getenv
from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

class DataBase(BaseSettings):
    DB_URL: str = getenv("DB_URL", f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3")

class Authorization(BaseSettings):
    SECRET_KEY: str = getenv("SECRET_KEY")
    SESSION_EXPIRE_SEC: int = 86_400

    EMEIL_CONFIRM_TIME_SEC: int = 43_200

    SESSION_AUTH_KEY: str = "Authorization"
    SESSION_DURATION_SEC: int = 86_400

class Email(BaseSettings):
    MAIL_USERNAME: str = getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = getenv("MAIL_PASSWORD"),
    MAIL_FROM: str = getenv("MAIL_FROM"),
    MAIL_PORT: int = getenv("MAIL_PORT"),
    MAIL_SERVER: str = getenv("MAIL_SERVER"),
    MAIL_FROM_NAME: str = "GoCode registering"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True


class Settings(BaseSettings):
    DEBUG: bool = True
    HOST: str = getenv("HOST", "127.0.0.1")
    PORT: int = getenv("PORT", 8000)

    DB: DataBase = DataBase()

    AUTH: Authorization = Authorization()

    EMAILS: Email = Email()


settings = Settings()
