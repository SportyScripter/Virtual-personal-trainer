from db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from models.exercise import Exercise
from schemas.excercise import ExerciseCreate
from models.body_part import BodyPart
from schemas.body_part import ResponseModelBodyPart

exercise_router = APIRouter(prefix="/exercises", tags=["exercises"])

exercise_router.post(
    "/create_exercise",
    status_code=status.HTTP_201_CREATED,
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
        description=exercise.description
    )
    
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    
    return {"message": "Exercise created successfully", "exercise": new_exercise}

