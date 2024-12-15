from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.repository import UserRepository
from api.users.views import router as users_api
from config.db import db_handler

app = FastAPI()

origins = ["http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_api)


@app.get("/")
async def read_root(session: AsyncSession = Depends(db_handler.get_session)):
    return await UserRepository().list(session)
