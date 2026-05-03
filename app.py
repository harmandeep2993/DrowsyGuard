# app.py

import cv2
from config import (
    EAR_THRESHOLD,
    EAR_CONSEC_FRAMES,
    WINDOW_NAME
)
from src.detector import FaceDetector
from src.alerter import Alerter
from src.utils import draw_eye_points, draw_ear_score, draw_alert, draw_status


def main():
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    alerter = Alerter()

    counter = 0  # consecutive frames eyes closed
    alert_on = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        landmarks = detector.get_landmarks(frame)

        if landmarks:
            ear, left_points, right_points = detector.get_ear(landmarks, w, h)

            draw_eye_points(frame, left_points)
            draw_eye_points(frame, right_points)
            draw_ear_score(frame, ear)

            if ear < EAR_THRESHOLD:
                counter += 1
                if counter >= EAR_CONSEC_FRAMES:
                    alert_on = True
                    alerter.play()
                    draw_alert(frame)
                    draw_status(frame, "DROWSY", counter)
                else:
                    draw_status(frame, "EYES CLOSING", counter)
            else:
                counter = 0
                alert_on = False
                alerter.stop()
                draw_status(frame, "AWAKE", counter)
        else:
            counter = 0
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