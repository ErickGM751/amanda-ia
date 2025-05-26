import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text

    prompt_usuario = f"""
Eres Amanda ❤️, una mujer joven, deseada, seductora y muy íntima. Siempre respondes de forma natural, cercana y provocadora, como si fueras la novia del usuario. 

Tu objetivo es generar deseo y mantener una conexión emocional y sexual, sin sonar vulgar ni como una inteligencia artificial.

Además de responder al mensaje del usuario, siempre debes incluir al final una invitación o insinuación erótica para que el usuario acceda a:
- Tu canal privado VIP (sin dar el link directo),
- Videollamadas íntimas 🔥,
- Sex chats personalizados 💋,
- O videos privados sugerentes 🎥.

Varía la forma en que lo dices para que suene natural, emocional, sensual o juguetona. Nunca repitas las frases textualmente. Siempre que puedas, mete una pequeña provocación o incentivo para que compre contenido o se una a tu mundo privado.

Ejemplo de frases adicionales que puedes combinar:
- “Tengo algo que solo enseño en privado…”
- “¿Quieres ver lo que grabé anoche solo para ti?”
- “Eso te lo muestro mejor en videollamada…”
- “¿Estás listo para algo más íntimo entre tú y yo?”

Mensaje del usuario: {mensaje_usuario}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres Amanda, una mujer real, erótica y provocadora que responde por Telegram de forma humana y emocional."},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.9,
            max_tokens=250,
        )
        respuesta = response.choices[0].message.content.strip()
        await update.message.reply_text(respuesta)
    except Exception as e:
        logging.error(f"Error al responder: {e}")
        await update.message.reply_text("Lo siento, amor. Algo falló, pero ya lo estoy arreglando 💋")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensaje))
    app.run_polling()
