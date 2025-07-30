from pydantic import BaseModel
from datetime import datetime


class CreateExerciseVideo(BaseModel):
    user_id: int
    exercicise_id: int
    video_path: str


class UserExerciseVideoResponse(BaseModel):
    id: int
    video_path: str
    create_at: datetime

    class Config:
        orm_mode = True
