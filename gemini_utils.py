import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gift_ideas_from_text(user_input):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = f"""You are an AI gift expert.
Given the following user input, extract their emotion, the occasion, and suggest 3–5 gift ideas.

Input: {user_input}

Respond in this format:
Emotion: ...
Occasion: ...
Gift Suggestions: ...
"""
    response = model.generate_content(prompt)
    return response.text

def get_gift_ideas_from_image(image_path, user_text=""):
    model = genai.GenerativeModel("models/gemini-1.5-pro-vision")
    with Image.open(image_path) as img:
        prompt = f"""You are an AI gift recommender.
Analyze the image and accompanying text to detect emotions and occasions.
Suggest 3–5 relevant gift ideas.

Text: {user_text}
"""
        response = model.generate_content([prompt, img])
    return response.text