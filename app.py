# app.py

import cv2
from config import (
    EAR_THRESHOLD,
    EAR_CONSEC_FRAMES,
    MAR_THRESHOLD,
    MAR_CONSEC_FRAMES,
    WINDOW_NAME
)
from src.detector import FaceDetector
from src.alerter import Alerter
from src.logger import SessionLogger

logger = SessionLogger()

from src.utils import (
    draw_eye_points,
    draw_ear_score,
    draw_alert,
    draw_status,
    draw_mouth_points,
    draw_yawn_alert,
    draw_mar_score
)


def main():
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    alerter = Alerter()

    ear_counter = 0
    yawn_counter = 0
    alert_on = False
    yawn_alert_on = False

    while True:
        ret, frame = cap.read()
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
            if ear < EAR_THRESHOLD:
                ear_counter += 1
                if ear_counter >= EAR_CONSEC_FRAMES:
                    alert_on = True
                    alerter.play()
                    draw_alert(frame)
                    draw_status(frame, "DROWSY", ear_counter)
                    if ear_counter == EAR_CONSEC_FRAMES:  # log only once per event
                        logger.log_event("DROWSY", ear, mar, ear_counter)
                else:
                    draw_status(frame, "EYES CLOSING", ear_counter)
            else:
                ear_counter = 0
                alert_on = False
                alerter.stop()
                draw_status(frame, "AWAKE", ear_counter)
                if yawn_counter == MAR_CONSEC_FRAMES:  # log only once per event
                    logger.log_event("YAWN", ear, mar, yawn_counter)

            # yawning logic
            if mar > MAR_THRESHOLD:
                # print(f"MAR: {mar:.2f}")
                yawn_counter += 1
                if yawn_counter >= MAR_CONSEC_FRAMES:
                    yawn_alert_on = True
                    draw_yawn_alert(frame)
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

        cv2.imshow(WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()