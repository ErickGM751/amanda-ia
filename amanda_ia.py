import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Servicios disponibles
servicios = {
    "vip": {
        "nombre": "❤️ Canal VIP",
        "precio": 300,
        "descripcion": "✨ Fotos y videos diarios xxx\n❤️ Contacto directo conmigo (WhatsApp)\n🎁 Descuentos exclusivos\n📞 Llamadas y videollamadas especiales",
        "pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
    },
    "videollamada": {
        "nombre": "📹 Videollamada",
        "precio": 500,
        "descripcion": "15 minutos de videollamada XXX intensamente privada y provocadora.",
        "pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
    },
    "sexchat": {
        "nombre": "💬 Sex Chat",
        "precio": 300,
        "descripcion": "Intercambio de fotos, audios, textos calientes en tiempo real.",
        "pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
    },
    "video_personalizado": {
        "nombre": "🎥 Video Personalizado",
        "precio": 500,
        "descripcion": "Video de 20 minutos haciendo lo que desees + acceso al VIP 15 días + entrega <12hrs.",
        "pago": "https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(f"{s['nombre']} (${s['precio']})", callback_data=key)] for key, s in servicios.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hola cariño 💖, soy *Amanda IA*, la asistente personal de Amanda.

Estos son nuestros servicios disponibles. Pulsa para más detalles:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    servicio = servicios.get(query.data)
    if servicio:
        text = (
            f"{servicio['nombre']} - ${servicio['precio']} MXN\n\n"
            f"Incluye:\n{servicio['descripcion']}\n\n"
            f"👉 Puedes pagar ahora mismo vía [Mercado Pago]({servicio['pago']})\n"
            "📩 O por transferencia, escríbeme a @ami_pra"
        )
        await query.edit_message_text(text=text, parse_mode="Markdown", disable_web_page_preview=False, reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("💳 Pagar ahora", url=servicio['pago']),
            InlineKeyboardButton("Transferencia", url="https://t.me/ami_pra")
        ]]))

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    if "vip" in user_text:
        await enviar_info_servicio(update, "vip")
    elif "sex chat" in user_text:
        await enviar_info_servicio(update, "sexchat")
    elif "videollamada" in user_text:
        await enviar_info_servicio(update, "videollamada")
    elif "video personalizado" in user_text or "video" in user_text:
        await enviar_info_servicio(update, "video_personalizado")
    else:
        await update.message.reply_text(
            "Estoy aquí para ayudarte a elegir el mejor servicio. Elige una opción del menú o pregúntame sobre cualquiera de ellos. 💬"
        )

async def enviar_info_servicio(update, clave):
    servicio = servicios.get(clave)
    if servicio:
        text = (
            f"{servicio['nombre']} - ${servicio['precio']} MXN\n\n"
            f"Incluye:\n{servicio['descripcion']}\n\n"
            f"👉 Puedes pagar ahora mismo vía [Mercado Pago]({servicio['pago']})\n"
            "📩 O por transferencia, escríbeme a @ami_pra"
        )
        await update.message.reply_text(text, parse_mode="Markdown", disable_web_page_preview=False, reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("💳 Pagar ahora", url=servicio['pago']),
            InlineKeyboardButton("Transferencia", url="https://t.me/ami_pra")
        ]]))

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ocurrió un error: {context.error}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    app.add_error_handler(error_handler)
    app.run_polling()

