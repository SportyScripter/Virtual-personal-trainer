import math
import cv2
import mediapipe as mp
import os
import numpy as np

os.environ["GLOG_minloglevel"] = "2"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

path1 = "video/MartwyCiagPrawidlowaTechnika.mp4"
path2 = "video/MartwyCiagZlaTechnika.mp4"


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


def video_analysis(path1, path2):

    good_points = 0
    bad_points = 0
    # Inicjalizacja MediaPipe
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils
    paused = False
    # Uruchomienie kamery
    cap1 = cv2.VideoCapture(path1)
    cap2 = cv2.VideoCapture(path2)
    while cap1.isOpened() and cap2.isOpened():
        if not paused:
            ret1, frame1 = cap1.read()
            ret, frame2 = cap2.read()

            if not ret1 or not ret:
                break
            height = min(frame1.shape[0], frame2.shape[0])
            frame1 = cv2.resize(
                frame1, (int(frame1.shape[1] * height / frame1.shape[0]), height)
            )
            frame2 = cv2.resize(
                frame2, (int(frame2.shape[1] * height / frame2.shape[0]), height)
            )

            # Wykrywanie szkieletu dla pierwszego wideo
            frame1_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            results1 = pose.process(frame1_rgb)

            frame2_rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            results2 = pose.process(frame2_rgb)

            if results1.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame1, results1.pose_landmarks, mp_pose.POSE_CONNECTIONS
                )
                right_shoulder_1 = get_landmark_coordinates(
                    mp_pose, results1, "RIGHT_SHOULDER", frame1
                )  # PRAWY BARK
                right_hip_1 = get_landmark_coordinates(
                    mp_pose, results1, "RIGHT_HIP", frame1
                )  # PRAWY BOK
                right_knee_1 = get_landmark_coordinates(
                    mp_pose, results1, "RIGHT_KNEE", frame1
                )  # PRAWE KOLANO
                angle_right_tehnique = calculate_angle(
                    right_shoulder_1.x,
                    right_shoulder_1.y,
                    right_hip_1.x,
                    right_hip_1.y,
                    right_knee_1.x,
                    right_knee_1.y,
                )

            # Wykrywanie szkieletu dla drugiego wideo

            if results2.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame2, results2.pose_landmarks, mp_pose.POSE_CONNECTIONS
                )
                right_shoulder_2 = get_landmark_coordinates(
                    mp_pose, results2, "RIGHT_SHOULDER", frame2
                )  # PRAWY BARK
                right_hip_2 = get_landmark_coordinates(
                    mp_pose, results2, "RIGHT_HIP", frame2
                )  # PRAWY BOK
                right_knee_2 = get_landmark_coordinates(
                    mp_pose, results2, "RIGHT_KNEE", frame2
                )  # PRAWE KOLANO
                angle_technique_to_check = calculate_angle(
                    right_shoulder_2.x,
                    right_shoulder_2.y,
                    right_hip_2.x,
                    right_hip_2.y,
                    right_knee_2.x,
                    right_knee_2.y,
                )
                if (
                    angle_technique_to_check * 0.99
                    < angle_right_tehnique
                    < angle_technique_to_check * 1.01
                ):
                    good_points += 1
                    cv2.putText(
                        frame2,
                        "Technika poprawna",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )
                else:
                    bad_points += 1
                    cv2.putText(
                        frame2,
                        "Technika niepoprawna",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                        cv2.LINE_AA,
                    )

            # Połączenie dwóch klatek w poziomie
            final_frame = cv2.hconcat([frame1, frame2])
            final_frame = cv2.resize(final_frame, (1280, 720))

            # Wyświetlenie obrazu
            cv2.imshow("Porównanie Techniki", final_frame)

            # Zatrzymanie programu klawiszem 'q'
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("p"):
            paused = False
    last_frame = frame1.copy() if ret1 else final_frame.copy()
    text = f"Scores: {(good_points/int(cap1.get(cv2.CAP_PROP_FRAME_COUNT)))*100}%"
    print(f"good points: {good_points}")
    print(f"bad points: {bad_points}")
    print(f"liczba klatek: {int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))}")
    cv2.putText(
        last_frame,
        text,
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.imshow("Porównanie Techniki", last_frame)
    cv2.waitKey(0)
    # Zwolnienie zasobów
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()


video_analysis(path1, path2)
#  RIGT_HIP - PRAWY BOK
#  LEFT_SHOULDER - LEWY BARK
#  RIGHT_KNEE - PRAWE KOLANO

# TODO Nie zapomnij o dopasowaniu liczby klatek do target_length


from scipy.interpolate import interp1d


def normalize_frames(frames, target_length):
    """Dopasowuje liczbę klatek do target_length."""
    x = np.linspace(0, len(frames) - 1, num=len(frames))
    f = interp1d(x, frames, axis=0, kind="linear")
    x_new = np.linspace(0, len(frames) - 1, num=target_length)
    return f(x_new)
