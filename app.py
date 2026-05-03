# app.py

import cv2
import time

from config import EAR_CONSEC_FRAMES, MAR_CONSEC_FRAMES, WINDOW_NAME
from src.logger import SessionLogger
from src.detector import FaceDetector
from src.alerter import Alerter
from src.calibrator import Calibrator
from src.utils import (
    draw_eye_points,
    draw_ear_score,
    draw_alert,
    draw_status,
    draw_mouth_points,
    draw_yawn_alert,
    draw_mar_score,
    draw_fps
)


def main():
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    alerter = Alerter()
    prev_time = 0
    logger = SessionLogger()

    # run calibration at startup
    calibrator = Calibrator(duration=10)
    print("Starting calibration...")
    ear_threshold, mar_threshold = calibrator.run(cap, detector)
    print(f"Calibration complete — EAR threshold: {ear_threshold}, MAR threshold: {mar_threshold}")

    ear_counter = 0
    yawn_counter = 0
    alert_on = False
    yawn_alert_on = False

    while True:
        ret, frame = cap.read()
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time
        if not ret:
            break

        h, w = frame.shape[:2]
        landmarks = detector.get_landmarks(frame)

        if landmarks:
            # EAR — drowsiness detection
            ear, left_points, right_points = detector.get_ear(landmarks, w, h)
            draw_eye_points(frame, left_points)
            draw_eye_points(frame, right_points)
            draw_ear_score(frame, ear)

            # MAR — yawning detection
            mar, mouth_points = detector.calculate_mar(landmarks, w, h)
            draw_mouth_points(frame, mouth_points)
            draw_mar_score(frame, mar)

            # drowsiness logic
            if ear < ear_threshold:
                ear_counter += 1
                if ear_counter >= EAR_CONSEC_FRAMES:
                    alert_on = True
                    alerter.play()
                    draw_alert(frame)
                    draw_status(frame, "DROWSY", ear_counter)
                    if ear_counter == EAR_CONSEC_FRAMES:
                        logger.log_event("DROWSY", ear, mar, ear_counter)
                else:
                    draw_status(frame, "EYES CLOSING", ear_counter)
            else:
                ear_counter = 0
                alert_on = False
                alerter.stop()
                draw_status(frame, "AWAKE", ear_counter)

            # yawning logic
            if mar > mar_threshold:
                yawn_counter += 1
                if yawn_counter >= MAR_CONSEC_FRAMES:
                    yawn_alert_on = True
                    draw_yawn_alert(frame)
                    if yawn_counter == MAR_CONSEC_FRAMES:
                        logger.log_event("YAWN", ear, mar, yawn_counter)
            else:
                yawn_counter = 0
                yawn_alert_on = False

        else:
            ear_counter = 0
            yawn_counter = 0
            alerter.stop()
            cv2.putText(
                frame,
                "No face detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

        draw_fps(frame, fps)
        cv2.imshow(WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()