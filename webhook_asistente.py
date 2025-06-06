from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
import os
import logging
import requests
from respuesta_asistente_gpt import generar_respuesta_asistente

router = APIRouter()

# Configuración desde entorno
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "asistente123")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

logging.basicConfig(level=logging.INFO)

# --- Verificación de webhook (GET) ---
@router.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge, status_code=200)
    return PlainTextResponse("Forbidden", status_code=403)

# --- Recepción de mensajes (POST) ---
@router.post("/webhook")
async def recibir_mensaje(request: Request):
    try:
        data = await request.json()
        logging.info("📥 JSON recibido:")
        logging.info(data)

        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        logging.info("🔎 VALUE recibido:")
        logging.info(value)

        messages = value.get("messages", [])
        if not messages:
            logging.warning("⚠️ No se encontró 'messages'. Probablemente es una actualización de estado.")
            return PlainTextResponse("EVENT_RECEIVED", status_code=200)

        mensaje = messages[0]
        texto_usuario = mensaje.get("text", {}).get("body", "")
        numero = mensaje.get("from")

        if texto_usuario and numero:
            respuesta = generar_respuesta_asistente(texto_usuario)
            enviar_respuesta(numero, respuesta)
            logging.info(f"✅ Respuesta enviada a {numero}")
        else:
            logging.warning("⚠️ El mensaje no contenía texto o número válido.")

        return PlainTextResponse("EVENT_RECEIVED", status_code=200)

    except Exception as e:
        logging.error(f"❌ Error procesando el webhook: {e}")
        return PlainTextResponse("Error interno", status_code=500)

# --- Función para enviar respuesta por WhatsApp ---
def enviar_respuesta(numero: str, mensaje: str):
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        logging.error("❌ WHATSAPP_TOKEN o WHATSAPP_PHONE_NUMBER_ID no están definidos.")
        return

    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": mensaje}
    }

    response = requests.post(url, headers=headers, json=payload)
    logging.info(f"📤 Respuesta enviada a {numero}: {response.status_code} - {response.text}")
