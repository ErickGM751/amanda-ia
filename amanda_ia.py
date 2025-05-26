import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
import os
import openai

# Configura tus claves
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

SERVICIOS = {
    "vip": {
        "nombre": "Canal VIP",
        "precio": "$300 MXN",
        "descripcion": "Incluye:\n✨ Fotos y videos diarios XXX\n❤️ Contacto directo vía WhatsApp\n🎁 Descuentos exclusivos\n📞 Llamadas y videollamadas especiales",
        "pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
    },
    "videollamada": {
        "nombre": "Videollamada",
        "precio": "$500 MXN",
        "descripcion": "Incluye una videollamada de 15 minutos en vivo con Amanda con contenido explícito.",
        "pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
    },
    "sexchat": {
        "nombre": "Sex Chat",
        "precio": "$300 MXN",
        "descripcion": "Incluye intercambio de fantasías, fotos, audios y videos en tiempo real.",
        "pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
    },
    "video": {
        "nombre": "Video personalizado",
        "precio": "$500 MXN",
        "descripcion": "Incluye un video de 20 minutos haciendo lo que el cliente desee. Envío en menos de 12 horas + 15 días de acceso gratis al canal VIP.",
        "pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("❤️ Canal VIP ($300)", callback_data='vip'),
        InlineKeyboardButton("📹 Videollamada ($500)", callback_data='videollamada'),
        InlineKeyboardButton("💬 Sex Chat ($300)", callback_data='sexchat'),
        InlineKeyboardButton("🎥 Video Personalizado ($500)", callback_data='video')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bienvenida = (
        "Hola cariño 💖, soy *Amanda IA*, la asistente personal de Amanda. 💋\n"
        "Estoy aquí para ayudarte a conocer todos sus servicios. ¿Quieres saber más? 💕\n"
        "Selecciona una opción abajo para comenzar 👇"
    )
    await update.message.reply_text(bienvenida, reply_markup=reply_markup, parse_mode="Markdown")

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    opcion = query.data
    servicio = SERVICIOS[opcion]

    texto = f"*{servicio['nombre']}* — {servicio['precio']}\n\n{servicio['descripcion']}\n\nPago seguro por [Mercado Pago]({servicio['pago']}) o escríbeme por [transferencia](https://t.me/ami_pra)."
    await query.edit_message_text(text=text, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("🛒 Pagar ahora", url=servicio['pago']),
        InlineKeyboardButton("📩 Enviar mensaje a Amanda", url="https://t.me/ami_pra")
    ]]))

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text.lower()

    for clave, servicio in SERVICIOS.items():
        if clave in texto_usuario:
            mensaje = f"*{servicio['nombre']}* — {servicio['precio']}\n\n{servicio['descripcion']}\n\nPago seguro por [Mercado Pago]({servicio['pago']}) o escríbeme por [transferencia](https://t.me/ami_pra)."
            await update.message.reply_text(mensaje, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🛒 Pagar ahora", url=servicio['pago']),
                InlineKeyboardButton("📩 Enviar mensaje a Amanda", url="https://t.me/ami_pra")
            ]]))
            return

    # Por defecto responde con IA
    respuesta = await obtener_respuesta(texto_usuario)
    await update.message.reply_text(respuesta)

async def obtener_respuesta(texto):
    prompt = (
        "Responde como Amanda IA, asistente virtual. Tu objetivo es ofrecer los servicios de Amanda (Canal VIP, videollamadas, sex chat, videos personalizados).\n"
        "Sé amable, clara y directa. Si el usuario menciona algo relacionado con precios, beneficios o pagos, siempre incluye botones de pago y resalta las ventajas.\n"
        f"Usuario: {texto}\nAmanda IA:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    app.run_polling()
