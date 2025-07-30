from pydantic import BaseModel
from typing import List
from datetime import datetime
from schemas.exercise_video import UserExerciseVideoResponse


class ExerciseCreate(BaseModel):
    exercise_name: str
    body_part_id: int
    description: str
    user_id: int


class ResponseModelExercise(BaseModel):
    id: int
    exercise_name: str
    body_part_id: int
    description: str

    class Config:
        orm_mode = True


class UserExerciseResponse(BaseModel):
    id: int
    exercise_name: str
    description: str | None
    body_part_name: str
    videos: List[UserExerciseVideoResponse] = []

    class Config:
        orm_mode = True
