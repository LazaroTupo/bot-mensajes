from fastapi import APIRouter, Request

router = APIRouter(prefix="/tiktok", tags=["tiktok"])

@router.post("/webhook")
async def receive_message(request: Request):
    """
    Endpoint para los Webhooks de TikTok.
    """
    body = await request.json()
    print("Recibido de TikTok:", body)
    return {"status": "success"}
