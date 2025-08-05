import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def list_gemini_models():
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("Error: GOOGLE_API_KEY no está configurada en las variables de entorno.")
        return

    genai.configure(api_key=google_api_key)

    try:
        for model in genai.list_models():
            if "generateContent" in model.supported_generation_methods:
                print(f"- {model.name}")
    except Exception as e:
        print(f"Error al listar modelos: {e}")

if __name__ == "__main__":
    list_gemini_models()