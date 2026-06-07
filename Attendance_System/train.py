import cv2
import os
import numpy as np

dataset_path = "dataset"

faces = []
labels = []

label_map = {}
current_id = 0

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

for person in os.listdir(dataset_path):
    

    person_folder = os.path.join(dataset_path, person)

    if not os.path.isdir(person_folder):
        continue

    label_map[current_id] = person

    for image_name in os.listdir(person_folder):

        image_path = os.path.join(person_folder, image_name)

        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (200, 200))
        faces.append(gray)
        labels.append(current_id)

    current_id += 1

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(
    faces,
    np.array(labels)
)

recognizer.save("trainer.yml")

np.save("labels.npy", label_map)

print("Training Complete!")