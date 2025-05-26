import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import os

# Variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Configurar logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Botones de pago
def botones_pago():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❤️ Canal VIP ($300)", callback_data="vip")],
        [InlineKeyboardButton("📹 Videollamada ($500)", callback_data="video")],
        [InlineKeyboardButton("💬 Sex Chat ($300)", callback_data="sexchat")],
        [InlineKeyboardButton("🎥 Video Personalizado ($500)", callback_data="personalizado")],
        [InlineKeyboardButton("✅ Pagar con Mercado Pago", url="https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044")],
        [InlineKeyboardButton("🏦 Transferencia / Hablar con Amanda", url="https://t.me/ami_pra")]
    ])

# Info detallada por servicio
DETALLE = {
    "vip": "✨ *Canal VIP – $300 MXN*\n• +200 fotos y videos XXX\n• Fotos y videos diarios\n• Número personal de WhatsApp\n• Descuentos en contenido adicional\n• Llamadas y videollamadas exclusivas",
    "video": "🎥 *Videollamada – $500 MXN*\n• 15 minutos en vivo contigo\n• Experiencia íntima totalmente personalizada",
    "sexchat": "💬 *Sex Chat – $300 MXN*\n• Conversación caliente al momento\n• Fotos, audios y videos exclusivos",
    "personalizado": "🎁 *Video Personalizado – $500 MXN*\n• 20 minutos haciendo lo que tú desees\n• Entrega en menos de 12 horas\n• Incluye 15 días gratis en Canal VIP"
}

# IA con tono formal pero amable
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    prompt = (
        "Eres Amanda IA, una asistente virtual con tono formal pero cariñoso. "
        "Respondes de forma breve y clara. Tu objetivo es ayudar al cliente a resolver dudas "
        "y ofrecer los servicios disponibles, explicando beneficios, precios y formas de pago cuando lo pidan. "
        f"Mensaje: {texto}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres una asistente virtual de ventas con tono humano y claro."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=180,
            temperature=0.8
        )
        await update.message.reply_text(response.choices[0].message.content.strip(), reply_markup=botones_pago())
    except Exception as e:
        logging.error(f"Error con OpenAI: {e}")
        await update.message.reply_text("Lo siento, algo falló. Puedes escribirme directamente a @ami_pra 💌")

# Mensaje de bienvenida
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "Hola cariño 💖, soy *Amanda IA*, la asistente personal de Amanda.

"
        "Estoy aquí para ayudarte a conocer sus servicios, resolver tus dudas y guiarte si deseas adquirir algo especial.

"
        "*Servicios disponibles:*
"
        "• Canal VIP – $300
"
        "• Videollamada – $500
"
        "• Sex Chat – $300
"
        "• Video Personalizado – $500

"
        "Haz clic en cualquiera de los botones para conocer más o realizar tu compra."
    )
    await update.message.reply_text(mensaje, reply_markup=botones_pago(), parse_mode="Markdown")

# Botones informativos
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data in DETALLE:
        await query.message.reply_text(DETALLE[data], parse_mode="Markdown", reply_markup=botones_pago())

# Setup
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", bienvenida))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    main()
