from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faststream.rabbit import ExchangeType

from api.shared.middlewares import auth_session
from api.users.views import router as users_api
from api.problems.views import router as problems_api
from config.settings import RabbitMQ, settings

from logging import getLogger

from logs.config import configure_logs

configure_logs()
logger = getLogger(__name__)


@asynccontextmanager
async def rabbitmq_lifespan():
    logger.info("RabbitMQ connection established")
    rabbit = RabbitMQ()
    await rabbit.get_connection()
    push_exchange = RabbitMQ.set_exchange("PUSH_EXCHANGE", "push", ExchangeType.DIRECT)
    pull_exchange = RabbitMQ.set_exchange("PUll_EXCHANGE", "pull", ExchangeType.DIRECT)
    await rabbit.get_broker().declare_exchange(push_exchange)
    await rabbit.get_broker().declare_exchange(pull_exchange)
    queue = RabbitMQ.set_queue("TESTING", "Testing")
    testing_queue = await rabbit.get_broker().declare_queue(queue)
    await testing_queue.bind(exchange="push", routing_key="push")
    await testing_queue.bind(exchange="pull")
    try:
        yield
    finally:
        await rabbit.get_broker().close()
        logger.info("RabbitMQ connection closed")

@asynccontextmanager
async def redis_lifespan():
    logger.info("Redis connection established")
    settings.REDIS.set_client("in_waiting", db=0)
    try:
        yield
    finally:
        await settings.REDIS.close_all()
        logger.info("Redis connection closed")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with rabbitmq_lifespan(), redis_lifespan():
        yield

app = FastAPI(lifespan=lifespan)

origins = ["http://127.0.0.1:8000", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(auth_session)

app.include_router(users_api)
app.include_router(problems_api)
