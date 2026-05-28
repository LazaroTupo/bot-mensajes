from fastapi import APIRouter, Request
from app.services.rasa_client import send_message_to_rasa

router = APIRouter(prefix="/tiktok", tags=["tiktok"])

@router.post("/webhook")
async def receive_message(request: Request):
    """
    Endpoint para los Webhooks de TikTok.
    """
    body = await request.json()
    
    # Verificamos si es un evento de nuevo mensaje
    if body.get("event") == "im.message.receive":
        data = body.get("data", {})
        sender_id = data.get("sender_id")
        
        # Extraemos el texto del mensaje
        message_data = data.get("message", {})
        user_message = message_data.get("text")
        
        if sender_id and user_message:
            print(f"\n[TIKTOK DM] Recibido de {sender_id}: {user_message}")
            
            # Enviamos el mensaje al Cerebro IA (Rasa)
            rasa_responses = await send_message_to_rasa(sender_id, user_message)
            
            for response in rasa_responses:
                print(f"🤖 [TIKTOK DM] Bot responde: {response.get('text')}")
                # TODO: Petición HTTP a la API de TikTok para enviar la respuesta.
    else:
        print("Recibido evento desconocido de TikTok:", body)

    return {"status": "success"}
