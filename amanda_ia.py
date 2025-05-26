import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI
import os

# Configurar logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Variables del entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Productos y precios
PRODUCTOS = {
    "vip": {
        "nombre": "❤️ Canal VIP",
        "precio": 300,
        "beneficios": "más de 200 fotos y videos XXX + número personal de WhatsApp",
    },
    "video": {
        "nombre": "📹 Videollamada",
        "precio": 500,
        "beneficios": "videollamada íntima y personalizada",
    },
    "sexchat": {
        "nombre": "💬 Sex Chat",
        "precio": 300,
        "beneficios": "conversación picante ilimitada",
    }
}

URL_PAGO = "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
CONTACTO = "@ami_pra"

# Botones principales
def botones_principales():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❤️ Canal VIP ($300)", callback_data="comprar_vip")],
        [InlineKeyboardButton("📹 Videollamada ($500)", callback_data="comprar_video")],
        [InlineKeyboardButton("💬 Sex Chat ($300)", callback_data="comprar_sexchat")]
    ])

# Mensaje promocional general
def generar_mensaje_producto(key):
    prod = PRODUCTOS[key]
    return (
        f"{prod['nombre']} - ${prod['precio']} MXN\n\n"
        f"Incluye: {prod['beneficios']}\n\n"
        f"Pago seguro por Mercado Pago:\n{URL_PAGO}\n\n"
        f"O por transferencia, escríbeme a {CONTACTO}"
    )

# IA responde con tono erótico + venta
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    prompt = (
        "Eres Amanda, una mujer erótica y vendedora. Tu tono es sensual, cálido, directo. "
        "Responde al siguiente mensaje como si fueras Amanda, con un mensaje coqueto que al mismo tiempo "
        "redirija al cliente a comprar uno de tus servicios (VIP, sexchat o videollamada). "
        "Sé breve pero seductora, como en un chat humano. No repitas precios ni links, ya se mostraron antes.\n\n"
        f"Mensaje del cliente: {texto}"
    )
    try:
        respuesta = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Responde como Amanda, una mujer sensual y vendedora."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.8
        )
        await update.message.reply_text(respuesta.choices[0].message.content.strip(), reply_markup=botones_principales())
    except Exception as e:
        logging.error(f"Error con OpenAI: {e}")
        await update.message.reply_text("Amor, algo falló... pero sigo aquí para ti. 😘", reply_markup=botones_principales())

# Mostrar opciones
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "Hola amor ❤️ Estoy aquí para complacerte... ¿Qué deseas explorar hoy?"
    await update.message.reply_text(mensaje, reply_markup=botones_principales())

# Manejar botones
async def manejar_botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("comprar_"):
        key = data.split("_")[1]
        mensaje = generar_mensaje_producto(key)
        await query.message.reply_text(mensaje)

# Configurar aplicación
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(manejar_botones))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    app.run_polling()

if __name__ == "__main__":
    main()
