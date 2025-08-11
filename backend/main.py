from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from db.session import engine
from db.base_class import Base
from core.config import settings
from auth.utils import JWT_SECRET_KEY, ALGORITHM
from models.token import Token
from functools import wraps
from routers.body_part_routers import seed_body_parts
from routers.role_routers import seed_roles
from db.session import SessionLocal
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
import os
from auth.routers import user_router
from routers.role_routers import role_routers
from routers.body_part_routers import body_part_router
from routers.exercise_routers import exercise_router
from routers.exercise_video_routers import exercise_video_router
from routers.user_routers import user_setting_router
from routers.analysis_routers import analysis_router

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
        seed_roles(db)
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
    static_files_path = "/videos"
    os.makedirs(static_files_path, exist_ok=True)
    app.mount("/videos", StaticFiles(directory=static_files_path), name="videos")
    app.mount(
        "/profile_images",
        StaticFiles(directory="/profile_images"),
        name="profile_images",
    )
    create_table()
    return app


app = start_application()


app.include_router(user_router)
app.include_router(role_routers)
app.include_router(body_part_router)
app.include_router(exercise_router)
app.include_router(exercise_video_router)
app.include_router(user_setting_router)
app.include_router(analysis_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


print("a", end=" ")
print("b", end=" ")
