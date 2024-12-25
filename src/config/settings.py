from os import getenv
from pathlib import Path

from faststream.rabbit import RabbitBroker, RabbitQueue
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import redis.asyncio as redis

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

class DataBase(BaseSettings):
    DB_URL: str = getenv("DB_URL")

class RabbitMQ(BaseSettings):
    RABBITMQ_URL: str = getenv("RABBITMQ_URL")

    RABBITMQ_BROKER: RabbitBroker = RabbitBroker(RABBITMQ_URL)

    @classmethod
    def set_queue(cls, name_attr: str, rout_key: str, auto_delete: bool =True, **kwargs):
        setattr(cls, name_attr, RabbitQueue(rout_key, auto_delete, **kwargs))

    def get_broker(self, name_attr: str = "RABBITMQ_BROKER") -> RabbitBroker:
        if hasattr(self, name_attr):
            return getattr(self, name_attr)
        else:
            raise AttributeError(f"No RabbitMQ broker found with name: {name_attr}")

class Redis:
    REDIS_HOST: str = getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = getenv("REDIS_PORT")
    REDIS_PASSWORD: str = getenv("REDIS_PASSWORD")

    def set_client(self, attr_name: str, db: int = 0, **kwargs):
        setattr(
            self,
            attr_name,
            redis.Redis(
                host=self.REDIS_HOST,
                port=self.REDIS_PORT,
                db=db,
                **kwargs,
            ),
        )

    async def close_all(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, redis.Redis):
                await attr.close()

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

    RABBITMQ: RabbitMQ = RabbitMQ()

    REDIS: Redis = Redis()


settings = Settings()
