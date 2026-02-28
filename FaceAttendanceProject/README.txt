Face Attendance Tracker (Python + OpenCV)
=========================================

This project is a simple Face Recognition Attendance System made in Python.
It lets you:
- Register new faces using your webcam
- Track attendance with face recognition
- Save attendance logs into a CSV file
- Pause & Continue scanning so duplicate entries are avoided


Requirements
------------
Install Python 3.8+ and the following libraries:

    pip install opencv-python
    pip install numpy


Project Structure
-----------------
FaceAttendanceProject/
│
├── main.py              # Main script
├── attendance.csv       # Attendance file (auto-updated)
├── known_faces/         # Folder where face images are stored
└── README.txt           # Project instructions


How to Run
----------
1. Unzip the project folder.
2. Open a terminal inside the folder.
3. Run:

    python main.py


How It Works
------------
1. When the program starts, you’ll see a menu:
   - Press 1 → Register a new face (takes one photo and saves it).
   - Press 2 → Track attendance (scans faces and marks them in attendance.csv).
2. During attendance tracking:
   - The system will recognize faces from known_faces/.
   - Once a person is detected, their Name + Timestamp is saved in attendance.csv.
   - Press 'c' to continue scanning after the first detection.
   - Press 'q' to quit.


Example Attendance File
-----------------------
Name,Timestamp
Aayush,2025-08-30 15:22:11
John,2025-08-30 15:24:05
