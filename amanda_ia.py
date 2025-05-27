import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from openai import OpenAI

# Configura logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Configuración de OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)

# Diccionario de servicios con estructura clara
servicios = {
    "canal_vip": {
        "titulo": "❤️ Canal VIP - $300 MXN",
        "descripcion": "✨ ¿Qué incluye el Canal VIP?\n- Más de 200 fotos y videos diarios XXX\n- Contacto directo por WhatsApp\n- Descuentos exclusivos en contenido\n- Acceso a llamadas y videollamadas especiales",
        "pago": [
            [InlineKeyboardButton("💳 Pagar por Mercado Pago", url="https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044")],
            [InlineKeyboardButton("📢 Transferencia (hablar con Amanda)", url="https://t.me/ami_pra")]
        ]
    },
    "videollamada": {
        "titulo": "📹 Videollamada - $500 MXN",
        "descripcion": "🔸 Incluye 15 minutos de videollamada XXX completamente personalizada, en vivo y con lo que más te excite.",
        "pago": [
            [InlineKeyboardButton("💳 Pagar por Mercado Pago", url="https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044")],
            [InlineKeyboardButton("📢 Transferencia (hablar con Amanda)", url="https://t.me/ami_pra")]
        ]
    },
    "sex_chat": {
        "titulo": "💬 Sex Chat - $300 MXN",
        "descripcion": "🔸 Incluye un delicioso intercambio de fantasías, con fotos, videos y audios del momento. Ideal para desatar tus deseos más salvajes.",
        "pago": [
            [InlineKeyboardButton("💳 Pagar por Mercado Pago", url="https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044")],
            [InlineKeyboardButton("📢 Transferencia (hablar con Amanda)", url="https://t.me/ami_pra")]
        ]
    },
    "video_personalizado": {
        "titulo": "🎥 Video Personalizado - $500 MXN",
        "descripcion": "🔸 Incluye:\n- Video de 20 minutos haciendo lo que desees\n- Entrega en menos de 12 horas\n- Acceso gratuito 15 días al Canal VIP",
        "pago": [
            [InlineKeyboardButton("💳 Pagar por Mercado Pago", url="https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044")],
            [InlineKeyboardButton("📢 Transferencia (hablar con Amanda)", url="https://t.me/ami_pra")]
        ]
    }
}

# Mensaje de bienvenida con menú
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("❤️ Canal VIP ($300)", callback_data='canal_vip')],
        [InlineKeyboardButton("📹 Videollamada ($500)", callback_data='videollamada')],
        [InlineKeyboardButton("💬 Sex Chat ($300)", callback_data='sex_chat')],
        [InlineKeyboardButton("🎥 Video personalizado ($500)", callback_data='video_personalizado')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bienvenida = ("Hola cariño 💖, soy *Amanda IA*, la asistente personal de Amanda.\n"
                  "Estoy aquí para ayudarte a conocer todos sus servicios exclusivos.\n"
                  "Puedes preguntarme por cualquiera de ellos o elegir una opción abajo. Estoy para consentirte. 💋")
    await update.message.reply_text(bienvenida, reply_markup=reply_markup, parse_mode="Markdown")

# Lógica de botones
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data

    if key in servicios:
        data = servicios[key]
        texto = f"*{data['titulo']}*\n{data['descripcion']}"
        await query.message.reply_text(texto, parse_mode="Markdown")
        await query.message.reply_text("Selecciona tu método de pago:", reply_markup=InlineKeyboardMarkup(data['pago']))

# IA para objeciones y preguntas abiertas
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt_base = (
        "Eres Amanda IA, asistente virtual de Amanda.\n"
        "Tu estilo es dulce, cercano, pero profesional. Tu objetivo es ayudar al cliente a elegir entre Canal VIP, Videollamada, Sex Chat o Video Personalizado.\n"
        "Siempre responde en máximo 3 líneas, con tono atractivo y llamado a la acción.\n"
        "Si el cliente menciona interés por algún servicio, responde con entusiasmo y agrega botones de pago.\n"
        "Si tiene dudas, resuelve con empatía y redirige a explorar servicios.\n"
    )

    user_message = update.message.text
    full_prompt = f"{prompt_base}\nCliente: {user_message}\nAmanda IA:"

    completion = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": full_prompt}]
    )
    respuesta = completion.choices[0].message.content

    await update.message.reply_text(respuesta)

# Main app
if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot corriendo...")
    app.run_polling()
