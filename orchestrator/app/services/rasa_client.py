import httpx
from app.core.config import settings

async def send_message_to_rasa(sender_id: str, message: str) -> list:
    """
    Envía un mensaje a Rasa mediante su canal REST y devuelve la lista de respuestas.
    """
    url = f"{settings.RASA_URL}/webhooks/rest/webhook"
    payload = {
        "sender": sender_id,
        "message": message
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Hacemos la petición POST al servidor de Rasa
            response = await client.post(url, json=payload, timeout=10.0)
            response.raise_for_status()
            
            # Rasa devuelve un Array de mensajes: [{'recipient_id': '123', 'text': 'Hola!'}]
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error comunicándose con Rasa: {e}")
            return []
