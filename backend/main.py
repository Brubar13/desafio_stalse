from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from db.database import Base, engine
from db.seed import seed_initial_data

from routes import routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    seed_initial_data()

    yield


app = FastAPI(
    title="Ticket Dashboard API",
    lifespan=lifespan,
)

origins = [ "http://localhost:5173","http://127.0.0.1:5173" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes, prefix="")