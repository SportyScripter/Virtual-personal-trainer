from pydantic import BaseModel


class CreateExercise(BaseModel):
    exercise_name: str
    body_part_id: int
    description: str
