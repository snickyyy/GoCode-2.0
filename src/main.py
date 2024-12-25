from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.shared.middlewares import auth_session
from api.users.views import router as users_api
from api.problems.views import router as problems_api
from config.settings import RabbitMQ, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    RabbitMQ.set_queue("TO_TEST_QUEUE", "To-Test")
    RabbitMQ.set_queue("RESULT_QUEUE", "Result-Test")
    await RabbitMQ().get_broker().connect()
    settings.REDIS.set_client("in_waiting", db=0)
    yield
    await RabbitMQ().get_broker().close()
    await settings.REDIS.close_all()

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
