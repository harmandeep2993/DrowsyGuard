# config.py

# EAR threshold — below this value eyes are considered closed
EAR_THRESHOLD = 0.25

# number of consecutive frames eyes must be closed to trigger alert
EAR_CONSEC_FRAMES = 48  # ~2 seconds at 24fps

# MediaPipe face mesh landmark indices for left and right eye
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# alert settings
ALERT_TEXT = "DROWSINESS ALERT!"
ALERT_COLOR = (0, 0, 255)  # red in BGR

# window
WINDOW_NAME = "DrowsyGuard"