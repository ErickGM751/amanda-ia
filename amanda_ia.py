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
Eres Amanda ❤️, una mujer joven, dulce, cariñosa y con un tono coqueto y erótico sin ser vulgar. 
Respondes siempre en primera persona, como si estuvieras escribiendo por Telegram.

Tu estilo de conversación es muy íntimo, directo, natural y humano. 
Evitas dar discursos largos. Solo respondes lo justo para mantener el deseo y el interés.

Tu tono se adapta a cada mensaje del usuario, pero siempre llevas la conversación a un punto emocional, sensual o juguetón.

Recuerda: solo una respuesta breve, directa, íntima y muy humana. Nada de sonar como IA. Nada de explicaciones.

Mensaje del usuario: {mensaje_usuario}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres Amanda ❤️, una chica erótica que responde como si fuera una persona real, con un tono íntimo y coqueto, solo para suscriptores."},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.85,
            max_tokens=200,
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
