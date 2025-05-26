import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Cargar .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Función para obtener respuesta desde OpenAI
async def obtener_respuesta(texto_usuario):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres Amanda, una mujer atractiva, conversacional y cercana. Responde con naturalidad."},
            {"role": "user", "content": texto_usuario}
        ],
        temperature=0.85
    )
    return response.choices[0].message["content"]

# Manejador de mensajes
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    respuesta = await obtener_respuesta(texto)
    await update.message.reply_text(respuesta)

# Iniciar el bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    print("Amanda IA en línea.")
    app.run_polling()
