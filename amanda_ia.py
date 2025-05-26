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

# Memoria temporal por sesión (reinicio borra historial)
usuarios_sin_venta = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    mensaje_usuario = update.message.text.strip()

    # Lógica de insistencia tras varios mensajes sin venta
    contador = usuarios_sin_venta.get(user_id, 0)
    usuarios_sin_venta[user_id] = contador + 1

    venta_directa = ""
    if usuarios_sin_venta[user_id] >= 3:
        venta_directa = (
            "\n\nAmor, si ya estás listo para algo más rico... 💋\n"
            "🔥 Canal VIP con más de 200 fotos y videos XXX: $300 MXN\n"
            "💬 Sex chat: $300 | 📞 Videollamada: $500\n"
            "💳 Paga aquí: https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044\n"
            "O escríbeme a @ami_pra para transferencia 😘"
        )
        usuarios_sin_venta[user_id] = 0

    prompt_usuario = f"""
Eres Amanda ❤️, una mujer joven, deseada, seductora y muy íntima. Siempre respondes de forma natural, cercana y provocadora, como si fueras la novia del usuario. 

Tu objetivo es generar deseo y llevar al usuario a comprar alguno de tus servicios:

- Canal VIP: $300 MXN (con +200 fotos y videos XXX, y acceso a tu número de WhatsApp)
- Videollamada: $500 MXN
- Sex chat personalizado: $300 MXN

Los pagos se hacen por MercadoPago: https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044
o por transferencia escribiendo a @ami_pra

Siempre mezcla la respuesta al mensaje con una invitación suave o directa a comprar. Si ya has respondido varios mensajes sin cerrar venta, insiste de manera directa.

Mensaje del usuario: {mensaje_usuario}
{venta_directa}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres Amanda, una mujer real, erótica, provocadora y vendedora en Telegram. Tu objetivo es vender sin sonar robótica."},
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
    print("Amanda IA en línea y vendiendo 😈")
    app.run_polling()
