import cv2
import numpy as np
import csv
from datetime import datetime

# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# Load labels
labels = np.load("labels.npy", allow_pickle=True).item()

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# Track attendance already marked
marked = set()

# Create CSV if it doesn't exist
try:
    open("attendance.csv", "r")
except FileNotFoundError:
    with open("attendance.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time"])


def mark_attendance(name):

    if name in marked:
        return

    now = datetime.now()

    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H:%M:%S")

    with open("attendance.csv", "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            name,
            date,
            time
        ])

    marked.add(name)

    print(f"Attendance Marked: {name}")


camera = cv2.VideoCapture(0)

while True:
    unknown_detected = False

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face,(200,200))
        label, confidence = recognizer.predict(face)
        print(
            f"Prediction: {labels.get(label, 'Unknown')} | Confidence: {confidence:.2f}"
        )

        if confidence < 60:

            name = labels.get(label,"Unknown")

            mark_attendance(name)

            text = f"{name}"

            color = (0, 255, 0)

        else:

            text = "Unknown - Press R"

            color = (0, 0, 255)

            unknown_detected = True

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            color,
            2
        )

        cv2.putText(
            frame,
            text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    cv2.imshow(
        "Attendance System",
        frame
    )

    key = cv2.waitKey(1) & 0xFF


    if key == ord('q'):
     break

    if key == ord('r') and unknown_detected:

        camera.release()
        cv2.destroyAllWindows()

        name = input("Enter New User Name: ")

        import os

        folder = os.path.join("dataset", name)

        os.makedirs(folder, exist_ok=True)
        import sys
        import subprocess
        subprocess.run([sys.executable,"register.py"])

        break
    
camera.release()
cv2.destroyAllWindows()