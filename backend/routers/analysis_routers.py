from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from db.session import get_db
from auth.utils import get_current_user
from models.user import User

analysis_router = APIRouter(prefix="/analysis", tags=["Video Analysis"])


@analysis_router.post("/compare-videos")
async def compare_videos(
    user_video: UploadFile = File(...),
    trainer_video_path: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(f"User {current_user.username} uploaded a video for comparison.")
    print(f"Trainer's video path: {trainer_video_path}")

    # --- MIEJSCE NA PRZYSZŁĄ LOGIKĘ ANALIZY WIDEO ---

    analysis_result_image_path = "/analysis_results/comparison_placeholder.png"

    return {
        "message": "Video received for analysis.",
        "user_video_filename": user_video.filename,
        "trainer_video_path": trainer_video_path,
        "result_image_url": analysis_result_image_path,
    }
