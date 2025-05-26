import os
import openai
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Configuración básica de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Cargar variables de entorno
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Función para obtener respuesta desde OpenAI
async def obtener_respuesta(texto_usuario):
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres Amanda, una mujer atractiva, conversacional y cercana. Responde con naturalidad."},
                {"role": "user", "content": texto_usuario}
            ],
            temperature=0.85
        )
        return response.choices[0].message["content"]
    except Exception as e:
        logging.error(f"Error al obtener respuesta de OpenAI: {e}")
        return "Ups, hubo un problema con la IA. Intenta más tarde."

# Manejador de mensajes
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto = update.message.text
        respuesta = await obtener_respuesta(texto)
