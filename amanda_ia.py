import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters
import openai
import os

# Configura tu clave de API de OpenAI y el token del bot de Telegram
token = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Memoria de productos
PRODUCTOS = {
    "vip": {
        "nombre": "Canal VIP",
        "precio": 300,
        "descripcion": "✨ Fotos y videos diarios xxx\n❤️ Número personal para contacto directo\n🎁 Descuentos exclusivos\n📞 Llamadas y videollamadas especiales"
    },
    "videollamada": {
        "nombre": "Videollamada",
        "precio": 500,
        "descripcion": "15 minutos de videollamada XXX donde tú eliges lo que deseas ver y vivir."
    },
    "sexchat": {
        "nombre": "Sex Chat",
        "precio": 300,
        "descripcion": "Intercambio erótico en texto con fotos, videos y audios del momento."
    },
    "video": {
        "nombre": "Video personalizado",
        "precio": 500,
        "descripcion": "🎥 Video de 20 minutos cumpliendo tus fantasías\n📦 Entrega en menos de 12 hrs\n🎁 Acceso gratis a Canal VIP por 15 días"
    }
}

ENLACE_MERCADO_PAGO = "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
USUARIO_TRANSFERENCIA = "@ami_pra"

# Función para generar el menú de botones
def generar_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❤️ Canal VIP ($300)", callback_data="vip")],
        [InlineKeyboardButton("📹 Videollamada ($500)", callback_data="videollamada")],
        [InlineKeyboardButton("💬 Sex Chat ($300)", callback_data="sexchat")],
        [InlineKeyboardButton("🎥 Video personalizado ($500)", callback_data="video")]
    ])

# Función para generar el mensaje de bienvenida
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola cariño 💖, soy *Amanda IA*, la asistente personal de Amanda. Estoy aquí para ayudarte a conocer todos sus servicios eróticos y exclusivos.\n\nEstos son los servicios disponibles:",
        reply_markup=generar_menu(),
        parse_mode="Markdown"
    )

# Función para responder a los botones
def obtener_info_producto(producto_key):
    producto = PRODUCTOS.get(producto_key)
    if not producto:
        return "Lo siento, no encontré ese servicio."

    mensaje = f"*{producto['nombre']}* - ${producto['precio']} MXN\n\n{producto['descripcion']}\n\n💳 Pago por Mercado Pago: [Haz clic aquí]({ENLACE_MERCADO_PAGO})\n📲 O por transferencia, escríbenos a {USUARIO_TRANSFERENCIA}"
    return mensaje

async def manejar_botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    producto_key = query.data
    texto = obtener_info_producto(producto_key)
    await query.edit_message_text(
        text=texto,
        parse_mode="Markdown",
        reply_markup=generar_menu()
    )

# Inicialización de la aplicación y registro de handlers
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(token).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bienvenida))
    app.add_handler(CallbackQueryHandler(manejar_botones))

    app.run_polling()
