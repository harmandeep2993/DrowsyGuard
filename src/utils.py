# src/utils.py

import cv2
import numpy as np
from config import ALERT_COLOR, ALERT_TEXT, EAR_THRESHOLD


def draw_eye_points(frame, points, color=(0, 255, 0)):
    """Draw eye landmark points on frame."""
    for point in points:
        cv2.circle(frame, point, 2, color, -1)


def draw_ear_score(frame, ear):
    """Display EAR value on frame."""
    color = (0, 255, 0) if ear >= EAR_THRESHOLD else (0, 0, 255)
    cv2.putText(
        frame,
        f"EAR: {ear:.2f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )


def draw_alert(frame):
    """Draw drowsiness alert overlay on frame."""
    h, w = frame.shape[:2]

    # red transparent overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 255), -1)
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

    # alert text centered
    text_size = cv2.getTextSize(ALERT_TEXT, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
    text_x = (w - text_size[0]) // 2
    text_y = (h + text_size[1]) // 2

    cv2.putText(
        frame,
        ALERT_TEXT,
        (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (255, 255, 255),
        3
    )


def draw_status(frame, status, counter):
    """Draw current status and frame counter."""
    cv2.putText(
        frame,
        f"Status: {status}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )
    cv2.putText(
        frame,
        f"Counter: {counter}",
        (10, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


def draw_mouth_points(frame, points, color=(0, 255, 255)):
    """Draw mouth landmark points on frame."""
    for point in points:
        cv2.circle(frame, point, 2, color, -1)


def draw_yawn_alert(frame):
    """Draw yawn alert overlay on frame."""
    h, w = frame.shape[:2]

    # orange transparent overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, h), (0, 165, 255), -1)
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

    # alert text centered
    text = "YAWN DETECTED!"
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
    text_x = (w - text_size[0]) // 2
    text_y = (h + text_size[1]) // 2

    cv2.putText(
        frame,
        text,
        (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (255, 255, 255),
        3
    )


def draw_mar_score(frame, mar):
    """Display MAR value on frame."""
    from config import MAR_THRESHOLD
    color = (0, 255, 0) if mar < MAR_THRESHOLD else (0, 165, 255)
    cv2.putText(
        frame,
        f"MAR: {mar:.2f}",
        (10, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )


def draw_fps(frame, fps):
    """Display FPS on frame."""
    cv2.putText(
        frame,
        f"FPS: {fps:.0f}",
        (frame.shape[1] - 100, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )