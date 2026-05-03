# src/calibrator.py

import cv2
import time


class Calibrator:
    def __init__(self, duration=10):
        self.duration = duration  # seconds to collect baseline

    def run(self, cap, detector):
        """Collect EAR and MAR baseline from user."""
        ear_values = []
        mar_values = []

        start_time = time.time()

        while True:
            elapsed = time.time() - start_time
            remaining = self.duration - int(elapsed)

            ret, frame = cap.read()
            if not ret:
                break

            h, w = frame.shape[:2]
            landmarks = detector.get_landmarks(frame)

            if landmarks:
                ear, _, _ = detector.get_ear(landmarks, w, h)
                mar, _ = detector.calculate_mar(landmarks, w, h)
                ear_values.append(ear)
                mar_values.append(mar)

            # draw calibration UI
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

            cv2.putText(frame, "CALIBRATING...", (w // 2 - 150, h // 2 - 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            cv2.putText(frame, "Keep eyes open, mouth closed",
                        (w // 2 - 200, h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Starting in {remaining}s...",
                        (w // 2 - 120, h // 2 + 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("DrowsyGuard", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            if elapsed >= self.duration:
                break

        # calculate thresholds from baseline
        if ear_values and mar_values:
            avg_ear = sum(ear_values) / len(ear_values)
            avg_mar = sum(mar_values) / len(mar_values)

            ear_threshold = round(avg_ear - 0.10, 3)
            mar_threshold = round(avg_mar + 0.25, 3)

            return ear_threshold, mar_threshold

        # fallback to defaults if no face detected
        return 0.25, 1.1