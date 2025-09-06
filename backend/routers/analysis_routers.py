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
    v1 = (p1.x - p2.x, p1.y - p2.y)
    v2 = (p3.x - p2.x, p3.y - p2.y)

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


def get_landmark(results, landmark_name):

    try:
        landmark_map = {
            "NOSE": 0,
            "LEFT_EYE_INNER": 1,
            "LEFT_EYE": 2,
            "LEFT_EYE_OUTER": 3,
            "RIGHT_EYE_INNER": 4,
            "RIGHT_EYE": 5,
            "RIGHT_EYE_OUTER": 6,
            "LEFT_EAR": 7,
            "RIGHT_EAR": 8,
            "MOUTH_LEFT": 9,
            "MOUTH_RIGHT": 10,
            "LEFT_SHOULDER": 11,
            "RIGHT_SHOULDER": 12,
            "LEFT_ELBOW": 13,
            "RIGHT_ELBOW": 14,
            "LEFT_WRIST": 15,
            "RIGHT_WRIST": 16,
            "LEFT_PINKY": 17,
            "RIGHT_PINKY": 18,
            "LEFT_INDEX": 19,
            "RIGHT_INDEX": 20,
            "LEFT_THUMB": 21,
            "RIGHT_THUMB": 22,
            "LEFT_HIP": 23,
            "RIGHT_HIP": 24,
            "LEFT_KNEE": 25,
            "RIGHT_KNEE": 26,
            "LEFT_ANKLE": 27,
            "RIGHT_ANKLE": 28,
            "LEFT_HEEL": 29,
            "RIGHT_HEEL": 30,
            "LEFT_FOOT_INDEX": 31,
            "RIGHT_FOOT_INDEX": 32,
        }

        if landmark_name in landmark_map:
            landmark_idx = landmark_map[landmark_name]
            return results.pose_landmarks.landmark[landmark_idx]
        return None
    except:
        return None


def analyze_orientation(
    left_point, right_point, ref_point, left_name, right_name, ref_name
):

    center_x = (left_point.x + right_point.x) / 2
    center_y = (left_point.y + right_point.y) / 2

    width = abs(left_point.x - right_point.x)
    height_diff = abs(left_point.y - right_point.y)

    # Adaptacyjne progi w zależności od typu punktów
    width_thresholds = {
        "SHOULDER": 0.12,
        "HIP": 0.10,
        "KNEE": 0.08,
        "ANKLE": 0.06,
        "ELBOW": 0.08,
    }

    threshold = 0.10
    for body_part, thresh in width_thresholds.items():
        if body_part in left_name:
            threshold = thresh
            break

    confidence = 0.5

    if width > threshold:
        if ref_name == "NOSE":
            nose_deviation = abs(ref_point.x - center_x)
            if nose_deviation < 0.05:  # nos w centrum
                confidence = min(0.9, 0.5 + width * 2)
                return "front", confidence
            else:
                confidence = min(0.7, 0.3 + width * 1.5)
                return "back", confidence
        else:
            confidence = min(0.8, 0.4 + width * 1.5)
            return "front", confidence

    else:
        ref_offset = ref_point.x - center_x

        offset_magnitude = abs(ref_offset)

        if offset_magnitude > 0.03:
            confidence = min(0.9, 0.6 + offset_magnitude * 5)

            if ref_offset < 0:
                return "left_profile", confidence
            else:
                return (
                    "right_profile",
                    confidence,
                )
        else:
            confidence = 0.4
            if ref_offset < 0:
                return "right_profile", confidence
            else:
                return "left_profile", confidence
    return "unknown", 0.0


def detect_orientation(results):

    if not results.pose_landmarks:
        return "unknown"

    # Wszystkie możliwe pary punktów do analizy (w kolejności priorytetów)
    landmark_pairs = [
        ("LEFT_SHOULDER", "RIGHT_SHOULDER"),
        ("LEFT_HIP", "RIGHT_HIP"),
        ("LEFT_KNEE", "RIGHT_KNEE"),
        ("LEFT_ANKLE", "RIGHT_ANKLE"),
        ("LEFT_ELBOW", "RIGHT_ELBOW"),
    ]

    reference_points = ["NOSE", "LEFT_EYE", "RIGHT_EYE", "LEFT_EAR", "RIGHT_EAR"]

    best_result = None
    best_confidence = 0

    for left_name, right_name in landmark_pairs:
        left_point = get_landmark(results, left_name)
        right_point = get_landmark(results, right_name)

        if left_point and right_point:
            for ref_name in reference_points:
                ref_point = get_landmark(results, ref_name)
                if ref_point:
                    orientation, confidence = analyze_orientation(
                        left_point,
                        right_point,
                        ref_point,
                        left_name,
                        right_name,
                        ref_name,
                    )

                    if confidence > best_confidence:
                        best_result = orientation
                        best_confidence = confidence

                    if confidence > 0.8:
                        return orientation

    if best_confidence < 0.5:
        asymmetry_result = analyze_asymmetry_universal(results)
        if asymmetry_result != "unknown":
            return asymmetry_result

    return best_result if best_result else "unknown"


def analyze_asymmetry_universal(results):

    if not results.pose_landmarks:
        return "unknown"

    # Zbierz wszystkie dostępne punkty z lewej i prawej strony
    left_landmarks = []
    right_landmarks = []
    center_landmarks = []

    # Mapowanie nazw punktów MediaPipe
    all_landmarks = [
        "LEFT_SHOULDER",
        "RIGHT_SHOULDER",
        "LEFT_ELBOW",
        "RIGHT_ELBOW",
        "LEFT_WRIST",
        "RIGHT_WRIST",
        "LEFT_HIP",
        "RIGHT_HIP",
        "LEFT_KNEE",
        "RIGHT_KNEE",
        "LEFT_ANKLE",
        "RIGHT_ANKLE",
        "LEFT_EYE",
        "RIGHT_EYE",
        "LEFT_EAR",
        "RIGHT_EAR",
    ]

    center_points = ["NOSE", "LEFT_EYE_INNER", "RIGHT_EYE_INNER"]

    # Zbierz punkty lewej i prawej strony
    for landmark_name in all_landmarks:
        point = get_landmark(results, landmark_name)
        if point:
            if "LEFT" in landmark_name:
                left_landmarks.append(point.x)
            elif "RIGHT" in landmark_name:
                right_landmarks.append(point.x)

    # Zbierz punkty centralne
    for landmark_name in center_points:
        point = get_landmark(results, landmark_name)
        if point:
            center_landmarks.append(point.x)

    # Analiza jeśli mamy wystarczająco punktów
    if len(left_landmarks) >= 2 and len(right_landmarks) >= 2:
        avg_left = sum(left_landmarks) / len(left_landmarks)
        avg_right = sum(right_landmarks) / len(right_landmarks)
        body_center = (avg_left + avg_right) / 2

        # Szerokość ciała
        body_width = abs(avg_left - avg_right)

        if body_width > 0.15:
            return "front"
        elif body_width > 0.08:
            if center_landmarks:
                avg_center = sum(center_landmarks) / len(center_landmarks)
                center_offset = avg_center - body_center

                if abs(center_offset) < 0.03:
                    return "front"
                elif center_offset < -0.03:
                    return "right_profile"
                else:
                    return "left_profile"
            return "front"
        else:
            if center_landmarks:
                avg_center = sum(center_landmarks) / len(center_landmarks)
                if avg_center < body_center - 0.02:
                    return "right_profile"
                elif avg_center > body_center + 0.02:
                    return "left_profile"

    return "unknown"


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

        orientation = detect_orientation(results1)
        frame_scores = []
        joints = {
            "ELBOW": ("SHOULDER", "ELBOW", "WRIST"),
            "SHOULDER": ("HIP", "SHOULDER", "ELBOW"),
            "HIP": ("SHOULDER", "HIP", "KNEE"),
            "KNEE": ("HIP", "KNEE", "ANKLE"),
        }

        sides = []
        if orientation == "left_profile":
            sides = ["LEFT_"]
        elif orientation == "right_profile":
            sides = ["RIGHT_"]
        elif orientation == "front":
            sides = ["LEFT_", "RIGHT_"]
        elif orientation == "back":
            sides = ["LEFT_", "RIGHT_"]

        if sides:
            information_text_user_, color = "Analiza...\n", (255, 255, 255)
            information_text_trainer = ""
            total_frames += 1
            y_offset = 50
            for side in sides:
                for joint, points in joints.items():
                    p1_name, p2_name, p3_name = (side + p for p in points)

                    trainer_p1, trainer_p2, trainer_p3 = (
                        get_landmark(results1, name)
                        for name in (p1_name, p2_name, p3_name)
                    )
                    user_p1, user_p2, user_p3 = (
                        get_landmark(results2, name)
                        for name in (p1_name, p2_name, p3_name)
                    )

                    trainer_angle = calculate_angle(trainer_p1, trainer_p2, trainer_p3)
                    user_angle = calculate_angle(user_p1, user_p2, user_p3)

                    if trainer_angle is not None and user_angle is not None:
                        information_text_trainer = (
                            f"{side}{joint} TRNR ANG: {trainer_angle:.1f}\n"
                        )
                        if abs(trainer_angle - user_angle) <= 5:
                            frame_scores.append(1)
                            information_text_user, color = (
                                f"{side}{joint}: OK, ANG: {user_angle:.1f}\n",
                                (0, 255, 0),
                            )

                        else:
                            frame_scores.append(0)
                            information_text_user, color = (
                                f"{side}{joint}: NOK, ANG: {user_angle:.1f}\n",
                                (0, 0, 255),
                            )
                        cv2.putText(
                            frame2,
                            information_text_user,
                            (50, y_offset),  # Zmieniono (50, 50) na (50, y_offset)
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            color,
                            2,
                            cv2.LINE_AA,
                        )
                        cv2.putText(
                            frame1,
                            information_text_trainer,
                            (50, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 255),
                            2,
                            cv2.LINE_AA,
                        )
                        y_offset += 50

            if frame_scores and (sum(frame_scores) / len(frame_scores)) > 0.75:
                good_points += 1
            else:
                good_points += 0

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
        out.write(combined_frame)
        last_combined_frame = combined_frame  # Zapisujemy ostatnią klatkę
    # Po przetworzeniu całego wideo, rysuje wynik na ostatniej klatce
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
            (1000, 50),
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
    # Przygotuj ścieżki
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

    # Uruchom analizę i stwórz wynikowe wideo
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
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        final_output_full_path,
    ]
    subprocess.run(command, check=True)

    os.remove(result_video_full_path)

    if not os.path.exists(final_output_full_path):
        raise HTTPException(
            status_code=500,
            detail="Video processing failed to create a streamable output file.",
        )

    result_url_path = f"/analysis_results/{final_video_filename}"

    return {
        "message": "Analysis complete. Playing the comparison video.",
        "result_video_url": result_url_path,
    }
