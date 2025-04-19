import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Virtual presonal trainer"
    PROJECT_VERISON: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "default_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "default_pass")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5433")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "default_db")
    DATABASE_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


settings = Settings()
