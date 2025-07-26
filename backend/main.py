from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from db.session import engine
from db.base_class import Base
from auth.routers import user_router
from core.config import settings
from auth.utils import JWT_SECRET_KEY, ALGORITHM
from models.token import Token
from functools import wraps
from routers.role_routers import role_routers
from routers.body_part_routers import seed_body_parts
from db.session import SessionLocal
from contextlib import asynccontextmanager

origins = ["http://localhost:5173"]


def create_table():
    try:
        Base.metadata.create_all(bind=engine)
        print("Table created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_body_parts(db)
        yield
    finally:
        db.close()


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        openapi_url="/api/v1/openapi.json",
        secret_key=JWT_SECRET_KEY,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    create_table()
    return app


app = start_application()


app.include_router(user_router)
app.include_router(role_routers)


@app.get("/")
async def root():
    return {"message": "Hello World"}


print("a", end=" ")
print("b", end=" ")
