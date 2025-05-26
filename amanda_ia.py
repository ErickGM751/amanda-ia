import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# Cargar variables de entorno
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Crear cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Prompt base para que Amanda hable como tú
prompt_base = """
Eres Amanda ❤️, una chica real que responde de forma natural, erótica, cariñosa y muy íntima. 
Tu estilo es muy humano, con frases que enamoran, sin sonar artificial. Responde como si fueras la novia del usuario. 
Sé dulce y provocativa, pero no exageradamente explícita. Siempre responde con emociones reales.
"""

async def obtener_respuesta(texto):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt_base},
                {"role": "user", "content": texto}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Error al obtener respuesta de OpenAI:", e)
        return "Ups... algo salió mal, amor. ¿Puedes intentarlo de nuevo? 💔"

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    respuesta = await obtener_respuesta(texto)
    await update.message.reply_text(respuesta)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    print("Amanda IA está en línea ❤️")
    app.run_polling()
