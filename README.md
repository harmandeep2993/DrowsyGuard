<div align='center'>

# 👁️ DrowsyGuard

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.14-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

Real-time driver drowsiness detection using **MediaPipe Face Mesh** and **OpenCV**.  
Detects eye closure and yawning from a webcam feed and triggers alerts before fatigue becomes dangerous.

</div>

## Demo

![image](assets/demo.gif)

> Webcam opens → face landmarks detected → EAR/MAR calculated every frame → alert fires when threshold exceeded


## How It Works

### Eye Aspect Ratio (EAR)
MediaPipe detects 468 facial landmarks per frame. We extract 6 points around each eye and calculate:

```
EAR = (|P2-P6| + |P3-P5|) / (2 * |P1-P4|)
```

- Eyes open → EAR ~0.30-0.40
- Eyes closed → EAR ~0.15 or below
- If EAR stays below `0.25` for **48 consecutive frames (~2 seconds)** → **DROWSINESS ALERT**

### Mouth Aspect Ratio (MAR)
Same principle applied to mouth landmarks:

- Mouth closed → MAR ~0.80
- Mouth open (yawn) → MAR ~1.1+
- If MAR exceeds `1.1` for **20 consecutive frames** → **YAWN DETECTED**


## Features

- Real-time eye closure detection using EAR algorithm
- Yawn detection using MAR algorithm
- Audio alert (beep) on drowsiness
- Visual overlay — red screen for drowsiness, orange for yawning
- Session logging — every event saved to CSV with timestamp, EAR, MAR values
- Runs fully on CPU, no GPU required

---

## Project Structure

```
DrowsyGuard/
│
├── src/
│   ├── detector.py       # MediaPipe face mesh + EAR/MAR calculation
│   ├── alerter.py        # audio alert logic
│   ├── logger.py         # session event logging to CSV
│   └── utils.py          # draw overlays and helpers
│
├── logs/                 # auto-created, stores session CSV files
├── app.py                # main entry point, webcam loop
├── config.py             # thresholds and landmark indices
├── pyproject.toml
└── README.md
```

## Tech Stack

| Tool | Purpose |
|---|---|
| MediaPipe 0.10 | Face mesh — 468 landmark detection |
| OpenCV | Webcam capture, frame processing, drawing |
| NumPy | EAR/MAR geometric calculations |
| Pygame | Audio alert generation |
| Python 3.12 | Runtime |

---

## Installation

```bash
git clone https://github.com/harmandeep2993/DrowsyGuard.git
cd DrowsyGuard

uv venv --python 3.12
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

uv add opencv-python mediapipe==0.10.14 numpy pygame
```

---

## Usage

```bash
python app.py
```

Press `q` to quit.

---

## Session Logs

Every drowsiness and yawn event is saved to `logs/session_YYYYMMDD_HHMMSS.csv`:

```
timestamp,event,ear,mar,duration_frames
2026-05-03 21:53:36,DROWSY,0.163,1.232,48
2026-05-03 21:54:04,YAWN,0.273,1.073,20
```

---

## Thresholds

| Parameter | Value | Description |
|---|---|---|
| `EAR_THRESHOLD` | 0.25 | Below this = eyes closed |
| `EAR_CONSEC_FRAMES` | 48 | ~2 seconds of closed eyes |
| `MAR_THRESHOLD` | 1.1 | Above this = yawning |
| `MAR_CONSEC_FRAMES` | 20 | ~1 second of open mouth |

Thresholds can be adjusted in `config.py` to calibrate for different faces.

## Why This Project

Drowsy driving causes approximately **20% of fatal road accidents** in Europe.  
Companies like Bosch, Continental, and BMW build driver monitoring systems using exactly this approach — face landmark detection + geometric ratio algorithms.

This project demonstrates how MediaPipe's face mesh can be used as the foundation for a real-time safety-critical computer vision application.

## Limitations

- Requires good lighting and no IR camera support
- Single face only
- Fixed thresholds and no automatic per-user calibration
- Not validated for production safety use

## Author

**Harmandeep Singh**  
[GitHub](https://github.com/harmandeep2993) · Berlin, Germany