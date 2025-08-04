# Stwórz nowy plik, np. routers/user.py

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime

from db.session import get_db
from auth.utils import get_current_user
from models.user import User
from auth.schemas import UserResponse 

user_setting_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_setting_router.post(
    "/upload-profile-image",
    response_model=UserResponse,
    summary="Upload or change user's profile picture"
)
async def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Pozwala zalogowanemu użytkownikowi na wgranie lub zmianę zdjęcia profilowego.
    Stare zdjęcie jest usuwane, jeśli istnieje.
    """
    storage_path = "/profile_images"
    os.makedirs(storage_path, exist_ok=True) 

    if current_user.profile_image and os.path.exists(current_user.profile_image):
        try:
            os.remove(current_user.profile_image)
        except OSError as e:
            print(f"Error deleting old profile picture: {e}")

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only .jpg, .jpeg, .png are allowed."
        )
    
    new_filename = f"user_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
    
    full_save_path = os.path.join(storage_path, new_filename)
    
    try:
        with open(full_save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {e}"
        )

    current_user.profile_image = full_save_path
    db.commit()
    db.refresh(current_user)

    return current_user