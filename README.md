# OmniBot: Orquestador de Mensajes y Cerebro de IA 🤖

Este proyecto es una arquitectura modular diseñada para manejar la automatización de Mensajes Directos (DMs) y Comentarios de redes sociales (Instagram y TikTok), apoyada por Inteligencia Artificial conversacional (Rasa).

## 🏗️ Arquitectura del Proyecto

El repositorio está dividido en dos servicios independientes:

1. **`orchestrator/` (El Enrutador - FastAPI)**: Recibe los Webhooks de Meta (Instagram) y TikTok, estructura los datos y hace de puente de comunicación.
2. **`rasa_bot/` (El Cerebro - Rasa)**: Analiza el lenguaje natural (NLU), detecta intenciones y decide el flujo de la conversación y las respuestas.

---

## 🚀 Requisitos Previos

Asegúrate de tener instalado [uv](https://github.com/astral-sh/uv), un gestor de paquetes de Python extremadamente rápido.

---

## 🏃‍♂️ Cómo Levantar el Entorno Local

Para que el bot funcione de manera local, **debes levantar ambos servicios en terminales separadas**.

### 1. Levantar el Cerebro (Rasa)
Abre una terminal nueva, ve a la carpeta de Rasa e inicia el servidor habilitando su API REST:

```bash
cd rasa_bot
# Esto levanta el servidor de Rasa en http://localhost:5005
uv run rasa run --enable-api
```
*(Nota: El primer arranque tomará unos segundos mientras carga el modelo de IA en memoria).*

### 2. Levantar el Orquestador (FastAPI)
Abre una segunda terminal, ve a la carpeta del orquestador y levanta el servidor web:

```bash
cd orchestrator
# Esto levanta FastAPI en http://localhost:8000
uv run uvicorn app.main:app --reload
```

---

## 🧪 Cómo Probar Localmente (Simulacro)

Con ambas terminales corriendo, abre una **tercera terminal** para simular que un usuario llamado "cliente_123" te acaba de enviar la palabra "hola" por DM en Instagram:

```bash
curl -X POST http://localhost:8000/instagram/webhook \
     -H "Content-Type: application/json" \
     -d '{
       "object": "instagram",
       "entry": [
         {
           "messaging": [
             {
               "sender": { "id": "cliente_123" },
               "message": { "text": "hola" }
             }
           ]
         }
       ]
     }'
```
Deberías ver en la consola del Orquestador cómo FastAPI recibe el mensaje, se lo envía a Rasa (puerto 5005) y recibe la respuesta lista para ser devuelta a Instagram.

---

## ⚙️ Configuración para Producción (Redes Sociales Reales)

Antes de conectar esto a tus cuentas de Instagram/TikTok en la vida real:

1. Expón tu orquestador local a internet utilizando **Ngrok** (`ngrok http 8000`).
2. Crea un archivo `.env` dentro de la carpeta `orchestrator/` con tus tokens de acceso reales:
   ```env
   INSTAGRAM_VERIFY_TOKEN=tu_token_secreto_aqui
   INSTAGRAM_ACCESS_TOKEN=token_generado_en_meta_developers
   TIKTOK_VERIFY_TOKEN=token_de_tiktok
   RASA_URL=http://localhost:5005
   ```
3. Registra la URL generada por Ngrok (ej. `https://1234.ngrok.app/instagram/webhook`) en el portal de Meta for Developers.
