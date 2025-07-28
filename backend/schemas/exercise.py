from pydantic import BaseModel


class ExerciseCreate(BaseModel):
    exercise_name: str
    body_part_id: int
    description: str
