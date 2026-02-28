# Face Attendance Project

A face recognition-based attendance tracking system built with Python and OpenCV.

## Features

- **Register new faces** - Capture and store face images using your webcam
- **Automatic attendance tracking** - Recognizes known faces and logs attendance
- **CSV export** - Attendance records saved with name and timestamp
- **Pause/Continue scanning** - Avoid duplicate entries with manual control

## Requirements

- Python 3.8+
- OpenCV
- NumPy

Install dependencies:
```bash
pip install opencv-python numpy
```

## Project Structure

```
FaceAttendanceProject/
├── main.py              # Main script
├── ui.py                # UI components
├── attendance.csv       # Attendance logs (auto-generated)
├── known_faces/         # Face images for recognition
└── README.md            # This file
```

## Usage

1. Run the program:
   ```bash
   python main.py
   ```

2. Menu options:
   - Press `1` → Register a new face
   - Press `2` → Start attendance tracking

3. During tracking:
   - Press `c` to continue scanning after detection
   - Press `q` to quit

## How It Works

1. Place known face images in `known_faces/` folder (naming the file as the person's name)
2. When running attendance mode, the system compares detected faces against known faces
3. Matched faces are logged to `attendance.csv` with timestamp

## Example attendance.csv

```
Name,Timestamp
Aayush,2025-08-30 15:22:11
John,2025-08-30 15:24:05
```
