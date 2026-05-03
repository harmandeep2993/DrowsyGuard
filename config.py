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

# Mouth landmark indices for yawning detection
MOUTH = [61, 291, 39, 181, 0, 17, 269, 405]

# MAR threshold — above this value mouth is considered open (yawning)
MAR_THRESHOLD = 1.1

# consecutive frames mouth must be open to trigger yawn alert
MAR_CONSEC_FRAMES = 20  # ~1 second at 20fps

# yawn alert text
YAWN_ALERT_TEXT = "YAWN DETECTED!"
YAWN_ALERT_COLOR = (0, 165, 255)  # orange in BGR

# window
WINDOW_NAME = "DrowsyGuard"