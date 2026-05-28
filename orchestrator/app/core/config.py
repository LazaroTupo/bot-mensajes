import os
import json
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "OmniBot Orchestrator"
    RASA_URL = os.getenv("RASA_URL", "http://localhost:5005")
    
    # Credenciales de Redes Sociales
    INSTAGRAM_VERIFY_TOKEN = os.getenv("INSTAGRAM_VERIFY_TOKEN", "mi_token_secreto")
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    
    # Credenciales de TikTok
    TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY", "")
    TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET", "")
    
    @property
    def tiktok_tokens(self) -> dict:
        tokens_json = os.getenv("TIKTOK_TOKENS_JSON", "{}")
        try:
            return json.loads(tokens_json)
        except json.JSONDecodeError:
            print("❌ Error al parsear TIKTOK_TOKENS_JSON. Asegúrate de que sea un JSON válido en tu .env.")
            return {}

settings = Settings()
