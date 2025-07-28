from db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Form, HTTPException, status, UploadFile, File
from models.exercises_video import ExerciseVideo
from schemas.exercise_video import CreateExerciseVideo
from models.user import User
from models.body_part import BodyPart
from models.exercise import Exercise
import datetime
import os
import asyncio

exercise_video_router = APIRouter(prefix="/exercise_videos", tags=["exercise_videos"])


async def createPathForUser(
    username: str, body_part_name: str, exercise_name: str
) -> str:
    current_dir = os.getcwd()
    base_path = os.path.join(current_dir, os.pardir, "users_videos")
    user_directory = os.path.join(base_path, username, body_part_name, exercise_name)
    return user_directory


# przerobić to by sprawdzało czy ścieżka już istnieje i jeśli tak to nie tworzyło kolejnej.
async def check_and_create_path_for_user(
    username: str,
    body_part_name: str,
    exercise_name: str,
):

    user_directory = await createPathForUser(username, body_part_name, exercise_name)
    if os.path.exists(user_directory):
        return user_directory
    elif not os.path.exists(user_directory):
        os.makedirs(user_directory)
    return user_directory


# Create a new exercise video
# async def create_exercise_video(
#     file: str,
#     user_id: int,
#     body_part_id: int,
#     exercise_id: int,
#     exercise_video: CreateExerciseVideo,
#     db: Session = Depends(get_db),
# ):
#     user = db.query(User).filter(User.id == user_id).first()
#     body_part = db.query(BodyPart).filter(BodyPart.id == body_part_id).first()
#     excercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
#     user_directory = await check_if_path_exists(
#         user.username, body_part.body_part_name, excercise.exercise_name, db
#     )
#     video_path = os.path.join(
#         user_directory, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
#     )
#     new_exercise_video = exercise_video(
#         user_id = user_id,
#         excercise_id = exercise_id,
#         video_path = video_path)
#     db.add(new_exercise_video)
#     db.commit()
#     db.refresh(new_exercise_video)
#     return {
#         "message": "Exercise video created successfully",
#     }


async def create_exercise_video(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    body_part_id: int = Form(...),
    exercise_id: int = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    body_part = db.query(BodyPart).filter(BodyPart.id == body_part_id).first()
    if not body_part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Body part not found",
        )
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    user_directory = await check_and_create_path_for_user(
        user.username, body_part.body_part_name, exercise.exercise_name
    )
    file_extension = os.path.splitext(file.filename)[1] if file.filename else ".mp4"
    file_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
    video_path = os.path.join(user_directory, file_name)
    try:
        with open(video_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}",
        )
    new_exercise_video = ExerciseVideo(
        user_id=user_id,
        exercise_id=exercise_id,
        video_path=video_path,
    )
    db.add(new_exercise_video)
    db.commit()
    db.refresh(new_exercise_video)
    return {
        "message": "Exercise video created successfully",
        "video_id": new_exercise_video.id,
        "video_path": video_path,
    }


@exercise_video_router.post("execise-videos")
async def create_exercise_video_endpoint(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    body_part_id: int = Form(...),
    exercise_id: int = Form(...),
    db: Session = Depends(get_db),
):
    return await create_exercise_video(
        file=file,
        user_id=user_id,
        body_part_id=body_part_id,
        exercise_id=exercise_id,
        db=db,
    )
