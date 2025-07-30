from db.session import get_db
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, APIRouter, HTTPException, status
from models.exercise import Exercise
from schemas.exercise import ExerciseCreate, ResponseModelExercise
from models.body_part import BodyPart
from auth.utils import get_current_user
from schemas.exercise import UserExerciseResponse
from typing import List
from models.user import User
import os

exercise_router = APIRouter(prefix="/exercise", tags=["Exercises"])


@exercise_router.post(
    "/create_exercise",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModelExercise,
)
async def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    body_part = db.query(BodyPart).filter(BodyPart.id == exercise.body_part_id).first()
    if not body_part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Body part not found",
        )

    new_exercise = Exercise(
        exercise_name=exercise.exercise_name,
        body_part_id=exercise.body_part_id,
        description=exercise.description,
        user_id=exercise.user_id,
    )

    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)

    return new_exercise


@exercise_router.delete("/delete_last_exercise", status_code=status.HTTP_204_NO_CONTENT)
async def delete_last_exercise(db: Session = Depends(get_db)):
    last_exercise = db.query(Exercise).order_by(Exercise.id.desc()).first()
    if not last_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No exercises found",
        )

    db.delete(last_exercise)
    db.commit()

    return {"message": "Last exercise deleted successfully"}


@exercise_router.get(
    "/my_exercises",
    response_model=List[UserExerciseResponse],
    summary="Pobierz wszystkie ćwiczenia zalogowanego użytkownika",
)
async def get_my_exercises(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
  
    exercises = (
        db.query(Exercise)
        .filter(Exercise.user_id == current_user.id)
        .options(joinedload(Exercise.body_part), joinedload(Exercise.exercise_videos))
        .all()
    )

    if not exercises:
        return []

    response_data = []
    for exercise in exercises:
        body_part_name = (
            exercise.body_part.body_part_name if exercise.body_part else "Brak partii"
        )

        response_data.append(
            {
                "id": exercise.id,
                "exercise_name": exercise.exercise_name,
                "description": exercise.description,
                "body_part_name": body_part_name,
                "videos": exercise.exercise_videos,
            }
        )

    return response_data


@exercise_router.delete(
    "/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Usuń ćwiczenie i powiązane wideo",
)
async def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise_to_delete = (
        db.query(Exercise)
        .options(joinedload(Exercise.exercise_videos))
        .filter(Exercise.id == exercise_id)
        .first()
    )

    if not exercise_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ćwiczenie nie znalezione."
        )

    if exercise_to_delete.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brak uprawnień do usunięcia tego zasobu.",
        )

    for video in exercise_to_delete.exercise_videos:
        if os.path.exists(video.video_path):
            try:
                os.remove(video.video_path)
            except OSError as e:
                print(f"Error deleting file {video.video_path}: {e}")

        db.delete(video)

    db.delete(exercise_to_delete)
    db.commit()

    return None 
