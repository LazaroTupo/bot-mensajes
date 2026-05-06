import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "OmniBot Orchestrator"
    RASA_URL = os.getenv("RASA_URL", "http://localhost:5005")
    
    # Credenciales de Redes Sociales
    INSTAGRAM_VERIFY_TOKEN = os.getenv("INSTAGRAM_VERIFY_TOKEN", "mi_token_secreto")
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    TIKTOK_VERIFY_TOKEN = os.getenv("TIKTOK_VERIFY_TOKEN", "")

settings = Settings()
