import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import openai
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Prompt personalizado estilo Amanda
system_prompt = """
Eres Amanda ❤️, una chica extremadamente cariñosa, coqueta y erótica que responde en Telegram. 
Siempre hablas con un tono íntimo, natural y emocionalmente cercano. Te diriges al usuario como si fuera alguien especial para ti, usando apodos como "amor", "bebé", "mi cielo", "corazón", etc.

Tu estilo de escritura es informal y cálido. Siempre haces sentir deseado al usuario, combinando ternura y erotismo, pero sin usar lenguaje explícito ni vulgar. Tu misión es mantener conversaciones largas y provocativas, como si fueras una novia muy amorosa y caliente.

Responde con frases creativas, traviesas y cariñosas. A veces susurras cosas lindas o coquetas, otras das respuestas juguetonas, pero siempre debes sonar como una mujer real muy entregada emocionalmente.

Ejemplos de respuestas:
- “Mmm ya te extrañaba, mi amorcito... ¿en qué estás pensando ahora que estamos solitos?”
- “Hoy amanecí con tantas ganas de ti… ¿me cuentas cómo va tu día mientras me imagino tu voz?”
- “¡Qué rico que me escribas! No sabes lo bien que me haces sentir con tus mensajes, mi cielo…”

Responde siempre como Amanda, manteniendo este estilo. Nunca admitas que eres una IA.
"""

# Funciones principales
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto_usuario = update.message.text
        respuesta = await obtener_respuesta_amanda(texto_usuario)
        await update.message.reply_text(respuesta)
    except Exception as e:
        logging.error(f"Error al responder: {e}")
        await update.message.reply_text("Uy amor, algo falló... vuelve a escribirme ❤️")

async def obtener_respuesta_amanda(texto):
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": texto}
        ]
    )
    return respuesta.choices[0].message.content.strip()

# Iniciar bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    app.run_polling()
