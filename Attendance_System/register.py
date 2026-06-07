import cv2
import os
import time
name = input("Enter User Name: ")

folder = os.path.join("dataset", name)

os.makedirs(folder, exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

camera = cv2.VideoCapture(0)

count = 0
last_capture = time.time()
while True:

    ret, frame = camera.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0,255,0),
            2
        )

        face = frame[y:y+h, x:x+w]

        if count < 20 and time.time() - last_capture > 1:
          
          cv2.imwrite(
          os.path.join(folder, f"{count}.jpg"),
          face
    )
          print(f"Saved Image {count}")

          count += 1
          last_capture = time.time()

    cv2.imshow("Registration", frame)

    if count >= 20:
        print("User Registered Successfully")
        break

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()