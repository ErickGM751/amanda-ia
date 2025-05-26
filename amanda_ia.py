import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

TOKEN = "AQUÍ_TU_TOKEN"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bienvenida = (
        "Hola cariño 💖, soy *Amanda IA*, la asistente personal de Amanda.

"
        "Estoy aquí para ayudarte a conocer todos sus servicios y resolver cualquier duda que tengas. "
        "Estos son los servicios disponibles:

"
        "❤️ Canal VIP ($300 MXN)
"
        "📸 Video personalizado ($500 MXN)
"
        "📞 Videollamada ($500 MXN)
"
        "💬 Sex Chat ($300 MXN)

"
        "Selecciona el que te interese para más detalles:"
    )
    botones = [
        [InlineKeyboardButton("❤️ Canal VIP ($300)", callback_data='vip')],
        [InlineKeyboardButton("📸 Video personalizado ($500)", callback_data='video')],
        [InlineKeyboardButton("📞 Videollamada ($500)", callback_data='llamada')],
        [InlineKeyboardButton("💬 Sex Chat ($300)", callback_data='sexchat')]
    ]
    await update.message.reply_text(bienvenida, reply_markup=InlineKeyboardMarkup(buttones), parse_mode='Markdown')

async def botones_servicios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'vip':
        texto = (
            "*Canal VIP - $300 MXN*

"
            "✨ Fotos y videos diarios XXX
"
            "📱 Número personal de WhatsApp
"
            "🎁 Descuentos exclusivos en contenido adicional
"
            "📞 Llamadas y videollamadas privadas

"
            "Pago seguro por Mercado Pago:"
        )
    elif data == 'video':
        texto = (
            "*Video personalizado - $500 MXN*

"
            "🎥 Video de 20 minutos con el contenido que tú quieras
"
            "🚀 Entrega en menos de 12 horas
"
            "🎁 Incluye acceso gratis por 15 días al Canal VIP

"
            "Pago seguro por Mercado Pago:"
        )
    elif data == 'llamada':
        texto = (
            "*Videollamada - $500 MXN*

"
            "📞 15 minutos de videollamada erótica
"
            "💋 Interacción íntima y personalizada

"
            "Pago seguro por Mercado Pago:"
        )
    elif data == 'sexchat':
        texto = (
            "*Sex Chat - $300 MXN*

"
            "🔥 Intercambio de fantasías, textos, fotos, videos y audios al momento
"
            "💦 Todo lo que imagines, solo por mensaje

"
            "Pago seguro por Mercado Pago:"
        )
    else:
        texto = "Servicio no reconocido."

    botones_pago = [
        [InlineKeyboardButton("💳 Pagar por MercadoPago", url="https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044")],
        [InlineKeyboardButton("📩 Transferencia", url="https://t.me/ami_pra")]
    ]

    await query.edit_message_text(text=texto, reply_markup=InlineKeyboardMarkup(botones_pago), parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones_servicios))
    app.run_polling()
