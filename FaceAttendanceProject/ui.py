import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime
import csv

# Paths
known_faces_dir = "known_faces"
os.makedirs(known_faces_dir, exist_ok=True)

# Ensure attendance file exists
if not os.path.exists("attendance.csv"):
    with open("attendance.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Timestamp"])

# Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ---------------- FACE FUNCTIONS ----------------
def register_face_ui():
    """Register a new face with a UI input for name"""
    name = simpledialog.askstring("Register Face", "Enter your name:")
    if not name:
        return

    cap = cv2.VideoCapture(0)
    saved = False
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, f"Press 's' to Save for {name}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

        cv2.imshow("Register Face", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("s") and len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(known_faces_dir, f"{name}.jpg"), face_img)
            messagebox.showinfo("Success", f"{name} registered successfully!")
            saved = True
            break
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    if not saved:
        messagebox.showwarning("Cancelled", "Face not saved!")

def track_attendance_ui():
    """Run attendance tracking"""
    known_faces = []
    known_names = []
    for filename in os.listdir(known_faces_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(known_faces_dir, filename)
            img = cv2.imread(img_path, 0)
            known_faces.append(img)
            known_names.append(os.path.splitext(filename)[0])

    if not known_faces:
        messagebox.showwarning("No Faces", "No registered faces found!")
        return

    cap = cv2.VideoCapture(0)

    while True:
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

            if best_match_name != "Unknown":
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("attendance.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([best_match_name, now])
                messagebox.showinfo("Attendance Marked", f"{best_match_name} marked present!")

                # ✅ Close window automatically after marking
                cap.release()
                cv2.destroyAllWindows()
                return

        cv2.imshow("Attendance Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def show_attendance():
    """Show attendance logs in a table"""
    if not os.path.exists("attendance.csv"):
        messagebox.showwarning("No Data", "No attendance file found yet!")
        return

    df = pd.read_csv("attendance.csv")
    top = tk.Toplevel(root)
    top.title("Attendance Records")
    top.geometry("450x300")
    top.configure(bg="#f8f9fa")

    tk.Label(top, text="Attendance Log", font=("Segoe UI", 14, "bold"), bg="#f8f9fa").pack(pady=10)

    tree = ttk.Treeview(top, columns=("Name", "Timestamp"), show="headings", height=10)
    tree.heading("Name", text="Name")
    tree.heading("Timestamp", text="Timestamp")

    tree.column("Name", width=150, anchor="center")
    tree.column("Timestamp", width=250, anchor="center")

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=(row["Name"], row["Timestamp"]))

    tree.pack(fill="both", expand=True, padx=10, pady=10)

def clear_attendance():
    """Clear all attendance logs"""
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear the attendance log?")
    if confirm:
        with open("attendance.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Timestamp"])  # Reset header
        messagebox.showinfo("Cleared", "Attendance log has been cleared!")

# ---------------- UI DESIGN ----------------
root = tk.Tk()
root.title("Face Attendance Tracker")
root.geometry("400x450")
root.configure(bg="#f0f2f5")

# Style
style = ttk.Style()
style.configure("TButton",
                font=("Segoe UI", 11, "bold"),
                padding=6)
style.map("TButton",
          background=[("active", "#1a73e8")],
          foreground=[("active", "white")])

# Title
tk.Label(root, text="Face Attendance Tracker", font=("Segoe UI", 18, "bold"), bg="#f0f2f5", fg="#1a73e8").pack(pady=30)

# Buttons
ttk.Button(root, text="➕ Register Face", command=register_face_ui).pack(pady=8, ipadx=10, ipady=5)
ttk.Button(root, text="📸 Track Attendance", command=track_attendance_ui).pack(pady=8, ipadx=10, ipady=5)
ttk.Button(root, text="📑 View Attendance Log", command=show_attendance).pack(pady=8, ipadx=10, ipady=5)
ttk.Button(root, text="🧹 Clear Attendance Log", command=clear_attendance).pack(pady=8, ipadx=10, ipady=5)
ttk.Button(root, text="❌ Exit", command=root.quit).pack(pady=8, ipadx=10, ipady=5)

root.mainloop()
