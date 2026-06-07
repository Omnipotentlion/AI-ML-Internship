from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


class Message(BaseModel):
    text: str


@app.post("/predict")
def predict(message: Message):

    sample_vector = vectorizer.transform([message.text])

    prediction = model.predict(sample_vector)

    if prediction[0] == 1:
        result = "Spam Message"
    else:
        result = "Not Spam"

    return {
        "prediction": result
    }