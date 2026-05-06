from fastapi import FastAPI
from app.api import instagram, tiktok
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Registrar los routers modulares
app.include_router(instagram.router)
app.include_router(tiktok.router)

@app.get("/")
async def root():
    return {"message": f"El {settings.PROJECT_NAME} está corriendo correctamente. 🚀"}
