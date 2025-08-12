from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from db.session import get_db
from auth.utils import get_current_user
from models.user import User
import math
import cv2
import mediapipe as mp
import os
import numpy as np
from scipy.interpolate import interp1d
import datetime
import shutil

analysis_router = APIRouter(prefix="/analysis", tags=["Video Analysis"])


def get_landmark_coordinates(mp_pose, results, landmark_name, frame):
    # """Funkcja pobierająca współrzędne wybranego punktu szkieletu."""
    if results.pose_landmarks:
        landmark = results.pose_landmarks.landmark[
            getattr(mp_pose.PoseLandmark, landmark_name)
        ]
        cv2.circle(
            frame,
            (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])),
            5,
            (255, 0, 0),
            -1,
        )
        return landmark
    return None


def calculate_angle(x1, y1, x2, y2, x3, y3):
    vector_a = (x1 - x2, y1 - y2)
    vector_b = (x3 - x2, y3 - y2)
    dot_product = vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1]
    magnitude_a = math.sqrt(vector_a[0] ** 2 + vector_a[1] ** 2)
    magnitude_b = math.sqrt(vector_b[0] ** 2 + vector_b[1] ** 2)

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    angle = math.degrees(math.acos(dot_product / (magnitude_a * magnitude_b)))

    return angle


def normalize_frames(frames, target_length):
    x = np.linspace(0, len(frames) - 1, num=len(frames))
    f = interp1d(x, frames, axis=0, kind="linear")
    x_new = np.linspace(0, len(frames) - 1, num=target_length)
    return f(x_new)


async def process_and_combine_videos(
    trainer_video_path: str, user_video_path: str, output_path: str
):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    cap1 = cv2.VideoCapture(trainer_video_path)
    cap2 = cv2.VideoCapture(user_video_path)

    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap1.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width1 * 2, height1))
    if not out.isOpened():
        print(
            f"BŁĄD: Nie można otworzyć pliku wideo do zapisu w ścieżce: {output_path}"
        )
        cap1.release()
        cap2.release()
        return

    while cap1.isOpened() and cap2.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        # Przetwarzanie klatek
        frame1_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        frame2_rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        # Przetwarzanie klatek przez MediaPipe Pose
        results1 = pose.process(frame1_rgb)
        results2 = pose.process(frame2_rgb)
        # narysowanie punktów szkieletu na klatkach
        if results1.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame1, results1.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

        if results2.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame2, results2.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

        # Dopasuj rozmiar klatki użytkownika do klatki trenera
        frame2_resized = cv2.resize(frame2, (width1, height1))

        # Połącz klatki horyzontalnie
        combined_frame = cv2.hconcat([frame1, frame2_resized])

        # Zapisz połączoną klatkę
        out.write(combined_frame)

    cap1.release()
    cap2.release()
    out.release()


@analysis_router.post("/compare-videos")
async def compare_videos(
    user_video: UploadFile = File(...),
    trainer_video_path: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Przygotuj ścieżki
    temp_dir = "/tmp/videos"
    results_dir = "/analysis_results"
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    user_video_temp_path = os.path.join(
        temp_dir, f"user_{current_user.id}_{timestamp}.mp4"
    )

    with open(user_video_temp_path, "wb") as buffer:
        shutil.copyfileobj(user_video.file, buffer)

    full_trainer_video_path = os.path.join("/videos", trainer_video_path)
    if not os.path.exists(full_trainer_video_path):
        raise HTTPException(status_code=404, detail="Trainer video not found")

    # 2. Uruchom analizę i stwórz wynikowe wideo
    result_video_filename = f"result_{current_user.id}_{timestamp}.mp4"
    result_video_full_path = os.path.join(results_dir, result_video_filename)

    await process_and_combine_videos(
        trainer_video_path=full_trainer_video_path,
        user_video_path=user_video_temp_path,
        output_path=result_video_full_path,
    )

    final_video_filename = f"final_{result_video_filename}"
    final_output_full_path = os.path.join(results_dir, final_video_filename)
    import subprocess

    command = [
        "ffmpeg",
        "-i",
        result_video_full_path,
        "-vcodec",
        "libx264",  # Użycie standardowego kodeka H.264
        "-pix_fmt",
        "yuv420p",  # Wymuś najbardziej kompatybilny format pikseli
        "-movflags",
        "+faststart",  # Przesuń metadane na początek
        final_output_full_path,
    ]
    subprocess.run(command, check=True)

    # Usuń nieprzetworzony plik
    os.remove(result_video_full_path)

    # Sprawdź, czy finalny plik istnieje
    if not os.path.exists(final_output_full_path):
        raise HTTPException(
            status_code=500,
            detail="Video processing failed to create a streamable output file.",
        )

    # Zwróć URL, używając samej nazwy pliku
    result_url_path = f"/analysis_results/{final_video_filename}"

    return {
        "message": "Analysis complete. Playing the comparison video.",
        "result_video_url": result_url_path,
    }
