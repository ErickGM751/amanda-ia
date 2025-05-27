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
        "descripcion": """💖 <b>Canal VIP</b> — $300 MXN / mes
🔓 Acceso a más de <b>200 fotos y videos XXX</b>
📲 Mi número personal de WhatsApp
📹 Videollamadas privadas
💬 Mensajes 24/7 conmigo
👉 <a href='https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044'>Ir al pago</a>""",
        "post_pago": InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Ya realicé mi pago", callback_data="vip_pagado")],
            [InlineKeyboardButton("❌ Tuve un error con el pago", callback_data="vip_error")]
        ])
    },
    "videollamada": {
        "nombre": "📞 Videollamada",
        "descripcion": """📞 <b>Videollamada 1 a 1</b> — $500 MXN
🎥 20 minutos privados contigo
🧴 Tú diriges, yo obedezco
💦 En tiempo real
➡️ Escríbeme: @ami_pra"""
    },
    "sex_chat": {
        "nombre": "💋 Sex Chat",
        "descripcion": """💋 <b>Sex Chat</b> — $300 MXN / 30 minutos
🔥 Audios + fotos + videos calientes
😈 Tú mandas... yo me entrego
📲 Todo por chat íntimo
➡️ Escríbeme: @ami_pra"""
    },
    "novia_virtual": {
        "nombre": "❤️‍🔥 Novia Virtual",
        "descripcion": """❤️‍🔥 <b>Novia Virtual</b> — $500 MXN / 2 semanas
💌 Trato de novio 24/7
📱 Mensajes, llamadas, contenido personalizado
🥺 Te cuido, te caliento, te provoco…
➡️ Escríbeme: @ami_pra"""
    },
    "video_personalizado": {
        "nombre": "🎬 Video Personalizado",
        "descripcion": """🎬 <b>Video Personalizado</b> — $500 MXN
⏱️ 20 minutos haciendo lo que tú digas
🎭 Desinhibida, obediente y entregada
📦 Entrega < 12 hrs
🎁 Incluye 15 días <b>GRATIS</b> en Canal VIP
➡️ Escríbeme: @ami_pra"""
    },
    "sextape": {
        "nombre": "📹 Sextape",
        "descripcion": """📹 <b>Sextape Privada</b>
🔥 Videos XXX de 15 a 30 minutos
👀 Solo para tus ojos
🧨 Hechos a tu medida
➡️ Escríbeme: @ami_pra"""
    }
}

# Botones de bienvenida
def obtener_teclado_servicios():
    botones = [[InlineKeyboardButton(s["nombre"], callback_data=key)] for key, s in SERVICIOS.items()]
    return InlineKeyboardMarkup(botones)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bienvenida = "Hola amor... soy <b>Amanda</b> 😈\n¿Quieres algo rico, privado y solo para ti? Tengo varios pecados que no se dicen... <i>se pagan</i> 🔥\n\nElige el que más se te antoje 👇"
    await update.message.reply_text(bienvenida, parse_mode="HTML", reply_markup=obtener_teclado_servicios())

# OpenAI con nueva API (v1)
async def responder_con_ia(mensaje_usuario):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt_base = """
Eres Amanda, una chica erótica, traviesa y cariñosa que vende contenido y servicios íntimos. Usa un tono sexy y atrevido. Si el cliente menciona un servicio específico, responde con la descripción adecuada.

Servicios disponibles:
""" + "\n".join([f"- {s['nombre']}: {s['descripcion']}" for s in SERVICIOS.values()]) + f"""

Cliente: {mensaje_usuario}
Amanda:
"""
    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt_base}]
    )
    return chat_completion.choices[0].message.content.strip()

# Mensajes de texto normales
async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = await responder_con_ia(update.message.text)
    await update.message.reply_text(respuesta, parse_mode="HTML")

# Botones: servicios + seguimiento
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "vip_pagado":
        await query.message.reply_text("Gracias amor ❤️ ya confirmé tu pago. Prepárate para algo delicioso... 😘", parse_mode="HTML")
    elif data == "vip_error":
        await query.message.reply_text("No te preocupes, bebé 😘 escribe directo a @ami_pra y te ayudo a resolverlo todo 💌", parse_mode="HTML")
    elif data in SERVICIOS:
        descripcion = SERVICIOS[data].get("descripcion", "Servicio no disponible.")
        markup = SERVICIOS[data].get("post_pago") if data == "canal_vip" else None
        await query.message.reply_text(descripcion, parse_mode="HTML", reply_markup=markup)
    else:
        await query.message.reply_text("Servicio no reconocido 😔", parse_mode="HTML")

# Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))
    app.run_polling()
