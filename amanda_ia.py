import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Configuración de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Cargar variables de entorno
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializar cliente OpenAI
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Función para obtener respuesta de OpenAI
async def obtener_respuesta(texto_usuario):
    try:
        respuesta = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres Amanda, una mujer atractiva, conversacional y cercana. Responde con naturalidad."},
                {"role": "user", "content": texto_usuario}
            ],
            temperature=0.85
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        logging.error(f"Error al obtener respuesta de OpenAI: {e}")
        return "Ups, hubo un error al hablar con Amanda. Intenta más tarde 💔"

# Función manejadora del mensaje de Telegram
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto = update.message.text
        respuesta = await obtener_respuesta(texto)
        await update.message.reply_text(respuesta)
    except Exception as e:
        logging.error(f"Error al manejar el mensaje: {e}")
        await update.message.reply_text("Ocurrió un error inesperado... 😢")

# Inicializar bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    print("Amanda IA en línea.")
    app.run_polling()
