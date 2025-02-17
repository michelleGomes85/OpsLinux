import google.generativeai as genai
import os

from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Constantes para chaves de API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def configure_model():

    genai.configure(api_key=GOOGLE_API_KEY)
    
    return genai.GenerativeModel(model_name="gemini-1.5-flash")

def ask_ai(prompt):

    model = configure_model()

    response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(response_mime_type='application/json')
                )
    
    return response.candidates[0].content.parts[0].text