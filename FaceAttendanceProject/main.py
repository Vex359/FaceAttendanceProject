import cv2
import os
import numpy as np
from datetime import datetime
import csv

# Ensure known_faces directory exists
known_faces_dir = "known_faces"
os.makedirs(known_faces_dir, exist_ok=True)

# Ensure attendance file exists
if not os.path.exists("attendance.csv"):
    with open("attendance.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Timestamp"])

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def register_face():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "Press 's' to Save", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

        cv2.imshow("Register Face", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("s") and len(faces) > 0:
            name = input("Enter your name: ")
            (x, y, w, h) = faces[0]
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(known_faces_dir, f"{name}.jpg"), face_img)
            print(f"{name} registered successfully!")
            cap.release()
            cv2.destroyAllWindows()
            return
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def track_attendance():
    known_faces = []
    known_names = []
    for filename in os.listdir(known_faces_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(known_faces_dir, filename)
            img = cv2.imread(img_path, 0)
            known_faces.append(img)
            known_names.append(os.path.splitext(filename)[0])

    cap = cv2.VideoCapture(0)
    marked_names = set()
    paused = False

    while True:
        if not paused:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                face_img_resized = cv2.resize(face_img, (100, 100))

                best_match_name = "Unknown"
                min_diff = float("inf")

                for known_face, name in zip(known_faces, known_names):
                    try:
                        known_face_resized = cv2.resize(known_face, (100, 100))
                        diff = np.sum((known_face_resized - face_img_resized) ** 2)
                        if diff < min_diff and diff < 1000000:
                            min_diff = diff
                            best_match_name = name
                    except:
                        continue

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, best_match_name, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                if best_match_name != "Unknown" and best_match_name not in marked_names:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("attendance.csv", "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([best_match_name, now])
                    marked_names.add(best_match_name)
                    print(f"Attendance marked for {best_match_name}")

            cv2.imshow("Attendance Tracker", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("p"):  # Pause
            paused = True
            print("Paused. Press 'c' to continue.")
        elif key == ord("c"):  # Continue
            paused = False

    cap.release()
    cv2.destroyAllWindows()

def main():
    print("Choose an option:")
    print("1. Register Face")
    print("2. Track Attendance")
    choice = input("Enter choice (1/2): ")

    if choice == "1":
        register_face()
    elif choice == "2":
        track_attendance()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
