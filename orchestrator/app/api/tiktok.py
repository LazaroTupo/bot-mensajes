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
                texto_respuesta = response.get('text')
                print(f"🤖 [TIKTOK DM] Bot responde: {texto_respuesta}")
                
                if token_a_usar:
                    # Hacemos la petición a la API de TikTok para enviar el mensaje de vuelta
                    # (Nota: La URL exacta puede variar según la versión de la API de TikTok, asegúrate de verificar en tu portal)
                    url_tiktok = "https://open.tiktokapis.com/v2/im/message/send/"
                    headers = {
                        "Authorization": f"Bearer {token_a_usar}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "recipient_id": sender_id,  # A quién le respondemos
                        "msg_type": "TEXT",
                        "content": json.dumps({"text": texto_respuesta})
                    }
                    
                    import httpx
                    async with httpx.AsyncClient() as client:
                        try:
                            res = await client.post(url_tiktok, json=payload, headers=headers)
                            print(f"✅ Respuesta enviada a TikTok. Status: {res.status_code}")
                            if res.status_code != 200:
                                print(f"Detalle del error de TikTok: {res.text}")
                        except Exception as e:
                            print(f"❌ Error al intentar enviar mensaje a TikTok: {e}")
    else:
        print("Recibido evento desconocido de TikTok:", body)

    return {"status": "success"}
