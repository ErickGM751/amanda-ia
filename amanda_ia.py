import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import openai

# Configuración inicial
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Diccionario de servicios
SERVICIOS = {
    "canal_vip": {
        "nombre": "🔥 Canal VIP",
        "descripcion": """💖 *Canal VIP* — $300 MXN / mes
🔓 Acceso a más de *200 fotos y videos XXX*
📲 Mi número personal de WhatsApp
📹 Videollamadas privadas
💬 Mensajes 24/7 conmigo
👉 [Ir al pago](https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044)"""
    },
    "videollamada": {
        "nombre": "📞 Videollamada",
        "descripcion": """📞 *Videollamada 1 a 1* — $500 MXN
🎥 20 minutos privados contigo
🧴 Tú diriges, yo obedezco
💦 En tiempo real
➡️ Escríbeme: @ami_pra"""
    },
    "sex_chat": {
        "nombre": "💋 Sex Chat",
        "descripcion": """💋 *Sex Chat* — $300 MXN / 30 minutos
🔥 Audios + fotos + videos calientes
😈 Tú mandas... yo me entrego
📲 Todo por chat íntimo
➡️ Escríbeme: @ami_pra"""
    },
    "novia_virtual": {
        "nombre": "❤️‍🔥 Novia Virtual",
        "descripcion": """❤️‍🔥 *Novia Virtual* — $500 MXN / 2 semanas
💌 Trato de novio 24/7
📱 Mensajes, llamadas, contenido personalizado
🥺 Te cuido, te caliento, te provoco…
➡️ Escríbeme: @ami_pra"""
    },
    "video_personalizado": {
        "nombre": "🎬 Video Personalizado",
        "descripcion": """🎬 *Video Personalizado* — $500 MXN
⏱️ 20 minutos haciendo lo que tú digas
🎭 Desinhibida, obediente y entregada
📦 Entrega < 12 hrs
🎁 Incluye 15 días *GRATIS* en Canal VIP
➡️ Escríbeme: @ami_pra"""
    },
    "sextape": {
        "nombre": "📹 Sextape",
        "descripcion": """📹 *Sextape Privada*
🔥 Videos XXX de 15 a 30 minutos
👀 Solo para tus ojos
🧨 Hechos a tu medida
➡️ Escríbeme: @ami_pra"""
    }
}

# Mensaje de bienvenida
def obtener_teclado_servicios():
    botones = [[InlineKeyboardButton(s["nombre"], callback_data=key)] for key, s in SERVICIOS.items()]
    return InlineKeyboardMarkup(botones)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bienvenida = "Hola amor... soy *Amanda* 😈\n¿Quieres algo rico, privado y solo para ti? Tengo varios pecados que no se dicen... *se pagan* 🔥\n\nElige el que más se te antoje 👇"
    await update.message.reply_text(bienvenida, parse_mode="Markdown", reply_markup=obtener_teclado_servicios())

# IA para responder mensajes
async def responder_con_ia(mensaje_usuario):
    prompt_base = """
Eres Amanda, una chica erótica, traviesa y cariñosa que vende contenido y servicios íntimos. Usa un tono sexy y atrevido. Si el cliente menciona un servicio específico, responde con la descripción adecuada.

Servicios disponibles:
""" + "\n".join([f"- {s['nombre']}: {s['descripcion']}" for s in SERVICIOS.values()]) + f"""

Cliente: {mensaje_usuario}
Amanda:
"""
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt_base}],
        max_tokens=250,
        temperature=0.8
    )
    return respuesta.choices[0].message.content.strip()

# Mensaje de texto recibido
async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = await responder_con_ia(update.message.text)
    await update.message.reply_text(respuesta, parse_mode="Markdown")

# Cuando toca un botón
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    servicio = query.data
    descripcion = SERVICIOS.get(servicio, {}).get("descripcion", "Servicio no disponible.")
    await query.message.reply_text(descripcion, parse_mode="Markdown")

# Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))
    app.run_polling()
