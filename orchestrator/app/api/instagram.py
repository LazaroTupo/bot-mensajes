from fastapi import APIRouter, Request, HTTPException, Query
from app.core.config import settings
from app.services.rasa_client import send_message_to_rasa

router = APIRouter(prefix="/instagram", tags=["instagram"])

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == settings.INSTAGRAM_VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Token de verificación inválido")

@router.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()
    
    if body.get("object") == "instagram":
        for entry in body.get("entry", []):
            
            # ==================================================
            # 1. Manejo de Mensajes Directos (DMs)
            # ==================================================
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event.get("sender", {}).get("id")
                
                if "message" in messaging_event and "text" in messaging_event["message"]:
                    user_message = messaging_event["message"]["text"]
                    print(f"\n[DM] Recibido de {sender_id}: {user_message}")
                    
                    # Rasa decide la respuesta
                    rasa_responses = await send_message_to_rasa(sender_id, user_message)
                    
                    for response in rasa_responses:
                        print(f"🤖 [DM] Bot responde: {response.get('text')}")
                        # TODO: Hacer petición HTTP a https://graph.facebook.com/v19.0/me/messages
                        # con el INSTAGRAM_ACCESS_TOKEN para enviar el DM.

            # ==================================================
            # 2. Manejo de Comentarios (Reels y Posts)
            # ==================================================
            for change_event in entry.get("changes", []):
                value = change_event.get("value", {})
                
                # Si el cambio es un comentario nuevo
                if change_event.get("field") == "comments":
                    comment_id = value.get("id")
                    comment_text = value.get("text")
                    from_username = value.get("from", {}).get("username")
                    
                    print(f"\n[COMENTARIO] @{from_username} comentó: {comment_text}")
                    
                    # Respuestas predeterminadas para comentarios
                    respuesta_comentario = "¡Hola! Te acabo de enviar toda la información por DM. 📩"
                    print(f"🤖 [COMENTARIO] Bot responde: {respuesta_comentario}")
                    
                    # TODO: 
                    # Paso A: Petición HTTP a https://graph.facebook.com/{comment_id}/replies para responder el comentario públicamente.
                    # Paso B: Petición HTTP a Meta para enviarle un DM al usuario usando su ID.
                        
    return {"status": "EVENT_RECEIVED"}
