from pydantic import BaseModel


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
