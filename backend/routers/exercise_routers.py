from db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from models.exercise import Exercise
from schemas.exercise import ExerciseCreate, ResponseModelExercise
from models.body_part import BodyPart

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
