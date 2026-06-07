import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_response(user_message, history=None):

    try:

        prompt = ""

        if history:

            for msg in history:
                prompt += f"{msg['role']}: {msg['content']}\n"

        prompt += f"user: {user_message}"

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"