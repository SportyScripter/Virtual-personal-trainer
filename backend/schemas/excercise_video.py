from pydantic import BaseModel

class CreateExerciseVideo(BaseModel):
    user_id: int
    exercicise_id: int
    video_path: str