import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)

SERVICIOS = {
    "canal_vip": {
        "precio": 300,
        "descripcion": "✨ Fotos y videos diarios xxx y dándome amor.\n❤️ Contacto directo conmigo: mi número personal de WhatsApp.\n🎁 Descuentos exclusivos en contenido adicional.\n📞 Llamadas y videollamadas especiales solo para ti.",
        "boton_pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044",
        "transferencia": "@ami_pra"
    },
    "videollamada": {
        "precio": 500,
        "descripcion": "Incluye 15 minutos de videollamada xxx para que disfrutemos juntos de algo muy personal y excitante.",
        "boton_pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044",
        "transferencia": "@ami_pra"
    },
    "sexchat": {
        "precio": 300,
        "descripcion": "Intercambio de fotos, audios y mensajes calientes en tiempo real. Muy íntimo, muy directo... 😈",
        "boton_pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044",
        "transferencia": "@ami_pra"
    },
    "video_personalizado": {
        "precio": 500,
        "descripcion": "Video de 20 min haciendo lo que tú desees. Entrega en menos de 12 hrs + acceso gratis 15 días al canal VIP.",
        "boton_pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044",
        "transferencia": "@ami_pra"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("❤️ Canal VIP ($300)", callback_data="canal_vip")],
        [InlineKeyboardButton("📹 Videollamada ($500)", callback_data="videollamada")],
        [InlineKeyboardButton("💬 Sex Chat ($300)", callback_data="sexchat")],
        [InlineKeyboardButton("🎥 Video Personalizado ($500)", callback_data="video_personalizado")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hola cariño 💖, soy *Amanda IA*, la asistente personal de Amanda.
Estoy aquí para ayudarte a descubrir todos sus servicios exclusivos. ¿Cuál te interesa conocer hoy?",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Eres Amanda IA, una asistente erótica pero profesional que ofrece servicios como canal VIP, videollamada, sex chat y videos personalizados. Cada mensaje debe ser corto y con intención de venta. Siempre incluye botones para pagar."
            },
            {"role": "user", "content": message}
        ],
        max_tokens=200
    )
    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

async def mostrar_servicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    servicio = SERVICIOS.get(query.data)
    if servicio:
        text = f"{servicio['descripcion']}

💳 Paga aquí: {servicio['boton_pago']}
💬 Transferencia: Escríbeme a {servicio['transferencia']}"
        await query.message.reply_text(text)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"❌ Ocurrió un error: {context.error}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.add_handler(CallbackQueryHandler(mostrar_servicio))
app.add_error_handler(error_handler)
app.run_polling()
