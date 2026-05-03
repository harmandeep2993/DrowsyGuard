# src/detector.py

import cv2
import mediapipe as mp
import numpy as np
from config import LEFT_EYE, RIGHT_EYE, EAR_THRESHOLD, MOUTH


class FaceDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def get_landmarks(self, frame):
        """Convert frame to RGB and run MediaPipe face mesh."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if results.multi_face_landmarks:
            return results.multi_face_landmarks[0].landmark
        return None

    def calculate_ear(self, landmarks, eye_indices, frame_w, frame_h):
        """Calculate Eye Aspect Ratio for given eye landmarks."""
        points = []
        for idx in eye_indices:
            x = int(landmarks[idx].x * frame_w)
            y = int(landmarks[idx].y * frame_h)
            points.append((x, y))

        # vertical distances
        A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
        B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))

        # horizontal distance
        C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))

        ear = (A + B) / (2.0 * C)
        return ear, points

    def get_ear(self, landmarks, frame_w, frame_h):
        """Get average EAR for both eyes."""
        left_ear, left_points = self.calculate_ear(landmarks, LEFT_EYE, frame_w, frame_h)
        right_ear, right_points = self.calculate_ear(landmarks, RIGHT_EYE, frame_w, frame_h)

        avg_ear = (left_ear + right_ear) / 2.0
        return avg_ear, left_points, right_points
    
    def calculate_mar(self, landmarks, frame_w, frame_h):
        """Calculate Mouth Aspect Ratio for yawning detection."""
        points = []
        for idx in MOUTH:
            x = int(landmarks[idx].x * frame_w)
            y = int(landmarks[idx].y * frame_h)
            points.append((x, y))

        # vertical distances
        A = np.linalg.norm(np.array(points[2]) - np.array(points[6]))
        B = np.linalg.norm(np.array(points[3]) - np.array(points[7]))
        C = np.linalg.norm(np.array(points[4]) - np.array(points[5]))

        # horizontal distance
        D = np.linalg.norm(np.array(points[0]) - np.array(points[1]))

        mar = (A + B + C) / (2.0 * D)
        return mar, points