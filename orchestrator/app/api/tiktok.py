from fastapi import APIRouter, Request
from app.services.rasa_client import send_message_to_rasa

router = APIRouter(prefix="/tiktok", tags=["tiktok"])

@router.post("/webhook")
async def receive_message(request: Request):
    """
    Endpoint para los Webhooks de TikTok.
    """
    # ====== LOGGING DE DEPURACIÓN ======
    print(f"\n{'='*40}")
    print("🔔 NUEVO WEBHOOK RECIBIDO DE TIKTOK")
    print(f"Headers: {dict(request.headers)}")
    try:
        raw_body = await request.body()
        print(f"Raw Body: {raw_body.decode('utf-8')}")
    except Exception as e:
        print(f"No se pudo leer el Raw Body: {e}")
    print(f"{'='*40}\n")
    # ===================================
    
    try:
        body = await request.json()
    except Exception:
        body = {}
        print("⚠️ Advertencia: TikTok envió un payload que no es JSON válido.")
    
    # Verificamos si es un evento de nuevo mensaje
    if body.get("event") == "im.message.receive" or body.get("event") == "tiktok.im.message.receive":
        import json
        
        # En TikTok, los detalles del mensaje vienen como un string JSON serializado en 'content'
        content_str = body.get("content", "{}")
        try:
            content_data = json.loads(content_str)
        except json.JSONDecodeError:
            content_data = {}
            
        sender_id = content_data.get("sender_id")
        user_message = content_data.get("text")
        
        # El receptor (tu cuenta comercial) viene en la raíz del payload
        receiver_id = body.get("user_openid")
        
        if sender_id and user_message:
            print(f"\n[TIKTOK DM] Recibido de {sender_id}: {user_message}")
            
            # Obtenemos el token correspondiente a la cuenta
            from app.core.config import settings
            token_a_usar = settings.tiktok_tokens.get(receiver_id)
            
            if not token_a_usar:
                print(f"⚠️ No hay token configurado para la cuenta {receiver_id}. Verifica tu TIKTOK_TOKENS_JSON.")
            else:
                print(f"✅ Usando token para la cuenta {receiver_id} para responder.")
            
            # Enviamos el mensaje al Cerebro IA (Rasa)
            rasa_responses = await send_message_to_rasa(sender_id, user_message)
            
            for response in rasa_responses:
                print(f"🤖 [TIKTOK DM] Bot responde: {response.get('text')}")
                # TODO: Petición HTTP a la API de TikTok para enviar la respuesta usando `token_a_usar`.
    else:
        print("Recibido evento desconocido de TikTok:", body)

    return {"status": "success"}
