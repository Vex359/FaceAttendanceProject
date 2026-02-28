# Face Attendance Tracker

A face recognition-based attendance system built with Python, OpenCV, and Tkinter. Automatically detects and recognizes faces to mark attendance.

## Features

- **Two Interface Modes**: CLI (terminal) and GUI (graphical)
- **Face Registration**: Capture and store face images via webcam
- **Face Recognition**: Automatically identifies registered faces
- **Attendance Logging**: Records name and timestamp to CSV
- **View Attendance**: Display records in a table format
- **Clear Logs**: Reset attendance records

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- NumPy
- Pandas (for GUI)
- Tkinter (included with Python)

Install dependencies:
```bash
pip install opencv-python numpy pandas
```

## Project Structure

```
FaceAttendanceProject/
├── main.py              # CLI version
├── ui.py                # GUI version (Tkinter)
├── attendance.csv       # Attendance logs
├── known_faces/         # Registered face images
└── README.md
```

## How to Run

### GUI Mode (Recommended)
```bash
python ui.py
```

### CLI Mode
```bash
python main.py
```

## GUI Controls

- **Register Face**: Click → Enter name → Press 's' to capture
- **Track Attendance**: Opens camera, auto-marks when face recognized
- **View Attendance Log**: Shows all records in a table
- **Clear Attendance Log**: Deletes all records (with confirmation)

## CLI Controls

### Main Menu
- Press `1` → Register a new face
- Press `2` → Track attendance

### Attendance Mode
- Press `p` → Pause scanning
- Press `c` → Continue scanning
- Press `q` → Quit

## How It Works

1. **Face Detection**: Uses Haar Cascade classifiers for face detection
2. **Face Recognition**: Compares detected faces against stored images using pixel difference
3. **Attendance Logging**: When a face is recognized, records name + timestamp to `attendance.csv`

## Face Registration

Name the image file as the person's name (e.g., `John.jpg`). The system will match based on the filename.

## Sample Output

**attendance.csv**:
```csv
Name,Timestamp
John,2025-08-30 15:22:11
Alice,2025-08-30 15:24:05
```

## License

MIT
