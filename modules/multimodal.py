import os
import time
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def analyze_image(uploaded_file):
    image = Image.open(uploaded_file)

    prompt = """
    You are a technical support assistant.

    Analyze this screenshot carefully.

    Extract:
    1. Screenshot type
    2. Error messages
    3. Important technical details
    4. Likely issue
    """

    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash"
    ]

    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[prompt, image]
            )
            return response.text

        except Exception as e:
            print(f"{model_name} failed: {e}")
            time.sleep(3)

    return "Could not analyze image because model is busy."