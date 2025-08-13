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


def get_landmark_coordinates(mp_pose, results, landmark_name):
    """Funckja pobierająca współrzędne (x, y) wybranego punktu szkieletu."""
    if results.pose_landmarks:
        try:
            landmark = results.pose_landmarks.landmark[
                getattr(mp_pose.PoseLandmark, landmark_name)
            ]
            return landmark.x, landmark.y
        except AttributeError:
            return None, None
    return None, None


def calculate_angle(p1, p2, p3):
    """Oblicza kąt w stopniach między trzema punktami (p2 jest wierzchołkiem)."""
    if p1 is None or p2 is None or p3 is None:
        return None

    # Wektory
    v1 = (p1[0] - p2[0], p1[1] - p2[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])

    # Iloczyn skalarny i magnitudy
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

    if magnitude_v1 * magnitude_v2 == 0:
        return 0

    # Kąt w radianach i stopniach
    angle_rad = math.acos(dot_product / (magnitude_v1 * magnitude_v2))
    angle_deg = math.degrees(angle_rad)

    return angle_deg


def normalize_frames(frames, target_length):
    x = np.linspace(0, len(frames) - 1, num=len(frames))
    f = interp1d(x, frames, axis=0, kind="linear")
    x_new = np.linspace(0, len(frames) - 1, num=target_length)
    return f(x_new)


async def process_and_combine_videos(
    trainer_video_path: str, user_video_path: str, output_path: str
):
    """Funkcja przetwarzająca wideo trenera i użytkownika, porównująca kąty i zapisująca wynik wideo."""
    good_points = 0
    total_frames = 0
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils
    # otwarcie plików wideo
    cap1 = cv2.VideoCapture(trainer_video_path)
    cap2 = cv2.VideoCapture(user_video_path)
    # pobranie wymiarów i fps pierwszego wideo
    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap1.get(cv2.CAP_PROP_FPS)
    # ustawinie kodeka i otwarcie pliku wideo do zapisu
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width1 * 2, height1))
    if not out.isOpened():
        print(
            f"BŁĄD: Nie można otworzyć pliku wideo do zapisu w ścieżce: {output_path}"
        )
        cap1.release()
        cap2.release()
        return
    # pętla do przetwarzania klatek wideo
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
        # --- ANALIZA KĄTÓW ---

        # 1. Pobierz współrzędne kluczowych stawów dla obu postaci
        trainer_shoulder = get_landmark_coordinates(mp_pose, results1, "RIGHT_SHOULDER")
        trainer_hip = get_landmark_coordinates(mp_pose, results1, "RIGHT_HIP")
        trainer_knee = get_landmark_coordinates(mp_pose, results1, "RIGHT_KNEE")

        user_shoulder = get_landmark_coordinates(mp_pose, results2, "RIGHT_SHOULDER")
        user_hip = get_landmark_coordinates(mp_pose, results2, "RIGHT_HIP")
        user_knee = get_landmark_coordinates(mp_pose, results2, "RIGHT_KNEE")

        # 2. Oblicz kąt w biodrze dla obu postaci
        trainer_angle = calculate_angle(trainer_shoulder, trainer_hip, trainer_knee)
        user_angle = calculate_angle(user_shoulder, user_hip, user_knee)

        # 3. Porównaj kąty i wyświetl informację na wideo użytkownika
        feedback_text = ""
        color = (255, 255, 255)  # biały

        if trainer_angle is not None and user_angle is not None:
            total_frames += 1
            if abs(trainer_angle - user_angle) <= 2:
                good_points += 1
                feedback_text = "Technika poprawna"
                color = (0, 255, 0)  # Zielony
            else:
                feedback_text = "Popraw blad!"
                color = (0, 0, 255)  # Czerwony

        # Wyświetl tekst na klatce użytkownika
        cv2.putText(
            frame2,
            feedback_text,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
            cv2.LINE_AA,
        )

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
        last_combined_frame = combined_frame  # Zapisujemy ostatnią klatkę
        out.write(combined_frame)
    # Po przetworzeniu całego wideo, rysujemy wynik na ostatniej klatce
    if last_combined_frame is not None and total_frames > 0:
        # Stwórz kopię ostatniej klatki
        final_frame_with_score = last_combined_frame.copy()

        score_percentage = (good_points / total_frames) * 100
        score_text = f"Wynik: {score_percentage:.1f}%"
        if score_percentage >= 80:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        # Rysuj wynik na nowej kopii
        cv2.putText(
            final_frame_with_score,
            score_text,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
            cv2.LINE_AA,
        )

        # Zapisz do wideo klatkę z wynikiem
        for _ in range(int(fps * 5)):
            out.write(final_frame_with_score)

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
