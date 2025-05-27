import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import openai

# Configura tu clave de API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Datos de los servicios
SERVICIOS = {
    "canal_vip": {
        "nombre": "❤️ Canal VIP ($300)",
        "descripcion": (
            "Incluye:
"
            "✨ Más de 200 fotos y videos diarios XXX
"
            "📞 Mi número personal de WhatsApp
"
            "🎁 Descuentos en contenido adicional
"
            "📱 Llamadas y videollamadas especiales"
        ),
        "precio": 300
    },
    "videollamada": {
        "nombre": "📹 Videollamada ($500)",
        "descripcion": "Incluye una videollamada XXX de 15 minutos en vivo conmigo 😘",
        "precio": 500
    },
    "sexchat": {
        "nombre": "💬 Sex Chat ($300)",
        "descripcion": "Intercambio de fotos, audios y mensajes subidos de tono totalmente personalizados 🔥",
        "precio": 300
    },
    "video_personalizado": {
        "nombre": "🎥 Video Personalizado ($500)",
        "descripcion": (
            "Incluye un video de 20 minutos haciendo lo que desees 🥵
"
            "⏱ Entrega en menos de 12 horas
"
            "🎁 Incluye acceso gratis de 15 días al Canal VIP"
        ),
        "precio": 500
    }
}

# URLs de pago
LINK_MERCADO_PAGO = "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
LINK_TRANSFERENCIA = "https://t.me/ami_pra"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(s["nombre"], callback_data=key)] for key, s in SERVICIOS.items()
    ]
    bienvenida = (
        "Hola cariño 💖, soy *Amanda IA*, la asistente personal de Amanda.

"
        "Estoy aquí para ayudarte a conocer todos los servicios disponibles y responder cualquier duda 😘.

"
        "Elige uno para saber más:"
    )
    await update.message.reply_text(bienvenida, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def mostrar_servicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    servicio = SERVICIOS.get(query.data)
    if servicio:
        texto = f"{servicio['nombre']}

{servicio['descripcion']}

"
        texto += f"👉 [Pagar con Mercado Pago]({LINK_MERCADO_PAGO})
"
        texto += f"👉 [Transferencia o duda]({LINK_TRANSFERENCIA})"
        await query.edit_message_text(text=texto, parse_mode="Markdown", disable_web_page_preview=True)

application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(mostrar_servicio))

if __name__ == "__main__":
    application.run_polling()
