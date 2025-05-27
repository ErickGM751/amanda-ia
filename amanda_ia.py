from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
import os
import logging
import openai

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token del bot
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Definición de servicios
SERVICIOS = {
    "canal_vip": {
        "titulo": "❤️ Canal VIP ($300)",
        "descripcion": "✨ Fotos y videos diarios xxx y dándome amor\n❤️ Contacto directo conmigo: mi número personal\n🎁 Descuentos exclusivos en contenido adicional\n📞 Llamadas y videollamadas especiales solo para ti.",
        "precio": "$300 MXN",
        "link_pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044",
        "contacto": "@ami_pra"
    },
    "videollamada": {
        "titulo": "📹 Videollamada ($500)",
        "descripcion": "Incluye 15 minutos de videollamada XXX, privada y personalizada solo para ti.",
        "precio": "$500 MXN",
        "link_pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044",
        "contacto": "@ami_pra"
    },
    "sexchat": {
        "titulo": "💬 Sex Chat ($300)",
        "descripcion": "Textos calientes, fotos al momento, audios íntimos y fantasías sin límites.",
        "precio": "$300 MXN",
        "link_pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044",
        "contacto": "@ami_pra"
    },
    "video_personalizado": {
        "titulo": "🎥 Video Personalizado ($500)",
        "descripcion": "Video de 20 minutos haciendo lo que desees\nEntrega en menos de 12 horas\nIncluye acceso gratuito al canal VIP por 15 días.",
        "precio": "$500 MXN",
        "link_pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044",
        "contacto": "@ami_pra"
    }
}

# Construir teclado de servicios
def construir_teclado():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(s["titulo"], callback_data=key)]
        for key, s in SERVICIOS.items()
    ])

# Menú inicial
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "Hola cariño 💕, soy *Amanda IA*, la asistente personal de Amanda.\n"
        "Estoy aquí para ayudarte a conocer los servicios más ricos y especiales.\n\n"
        "¿Qué te gustaría explorar hoy? Elige una opción o pregúntame lo que desees."
    )
    await update.message.reply_text(mensaje, reply_markup=construir_teclado(), parse_mode="Markdown")

# Manejo de botones
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data
    servicio = SERVICIOS.get(key)

    if servicio:
        texto = (
            f"*{servicio['titulo']}*\n"
            f"{servicio['descripcion']}\n\n"
            f"💸 Precio: {servicio['precio']}\n"
            f"[Pagar por Mercado Pago]({servicio['link_pago']})\n"
            f"O escríbeme directo: {servicio['contacto']}"
        )
        await query.edit_message_text(text=texto, parse_mode="Markdown", disable_web_page_preview=True)

# Función para generar respuestas con IA
async def generar_respuesta_ia(texto):
    openai.api_key = OPENAI_API_KEY
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres Amanda IA, la asistente personal de Amanda. Tu tono es sensual, breve y profesional. Promocionas servicios (VIP, sex chat, videollamada, video personalizado) resolviendo dudas, sugiriendo compras y mostrando beneficios. Siempre finaliza con botones de compra."},
                {"role": "user", "content": texto}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        logging.error(f"Error IA: {e}")
        return "Algo falló amor… pero sigo aquí para ti. 😘"

# Chat libre con IA
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    respuesta = await generar_respuesta_ia(user_input)
    await update.message.reply_text(respuesta, reply_markup=construir_teclado(), parse_mode="Markdown")

# Inicializar
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))
    logging.info("Amanda IA lista 💋")
    app.run_polling()
