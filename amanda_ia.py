import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, CallbackQueryHandler, filters
import os
import openai

# Configura tu clave de API
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Información de servicios
SERVICIOS = {
    "vip": {
        "nombre": "❤️ Canal VIP",
        "precio": 300,
        "descripcion": "Incluye:
✨ Fotos y videos diarios XXX
❤️ Contacto directo vía WhatsApp
🎁 Descuentos exclusivos
📞 Llamadas y videollamadas especiales",
    },
    "videollamada": {
        "nombre": "📹 Videollamada",
        "precio": 500,
        "descripcion": "15 minutos de videollamada XXX, totalmente personalizada.",
    },
    "sexchat": {
        "nombre": "💬 Sex Chat",
        "precio": 300,
        "descripcion": "Intercambio de textos, fotos, audios calientes y atención exclusiva.",
    },
    "video": {
        "nombre": "🎥 Video personalizado",
        "precio": 500,
        "descripcion": "Video de 20 minutos haciendo lo que desees 😈, entrega en <12h y acceso VIP por 15 días.",
    }
}

# Botones base
def botones_servicios():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(s["nombre"] + f" (${s['precio']})", callback_data=key)] for key, s in SERVICIOS.items()
    ])

# Mensaje de bienvenida
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bienvenida = (
        "Hola cariño 💖, soy *Amanda IA*, la asistente personal de Amanda.

"
        "Estoy aquí para ayudarte a elegir el servicio que más te guste:
"
    )
    await update.message.reply_text(bienvenida, reply_markup=botones_servicios(), parse_mode="Markdown")

# Manejador de botones
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data
    servicio = SERVICIOS.get(key)
    if servicio:
        mensaje = (
            f"{servicio['nombre']} – ${servicio['precio']} MXN

"
            f"{servicio['descripcion']}

"
            "Pago seguro por Mercado Pago:
"
            "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044

"
            "O por transferencia, escríbele directamente a: @ami_pra"
        )
        await query.edit_message_text(mensaje)

# Genera respuesta automática con GPT
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "Eres Amanda IA, una asistente virtual femenina que representa a Amanda. "
                    "Hablas de forma sugerente, directa, pero formal y profesional. "
                    "Tu objetivo principal es vender servicios como Canal VIP, Sex Chat, Videollamadas y Videos personalizados. "
                    "Siempre que sea posible, al finalizar cada mensaje muestra botones para contratar."
                )},
                {"role": "user", "content": texto}
            ],
            max_tokens=300
        )
        mensaje = respuesta.choices[0].message.content
        await update.message.reply_text(mensaje, reply_markup=botones_servicios())
    except Exception as e:
        logging.error(f"Error al generar respuesta: {e}")
        await update.message.reply_text("Lo siento, amor... hubo un problema al responderte, pero ya estoy aquí para ti.")

# Configuración del bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    main()
