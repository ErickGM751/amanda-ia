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
    "Canal VIP": {
        "descripcion": "💖 *Canal VIP* — $300 MXN / mes\n🔓 Acceso a más de *200 fotos y videos XXX*\n📲 Mi número personal de WhatsApp\n📹 Videollamadas privadas\n💬 Mensajes 24/7 conmigo\n👉 [Ir al pago](https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044)",
        "boton": "🔥 Canal VIP"
    },
    "Videollamada": {
        "descripcion": "📞 *Videollamada 1 a 1* — $500 MXN\n🎥 20 minutos privados contigo\n🧴 Tú diriges, yo obedezco\n💦 En tiempo real\n➡️ Escríbeme: @ami_pra",
        "boton": "📞 Videollamada"
    },
    "Sex Chat": {
        "descripcion": "💋 *Sex Chat* — $300 MXN / 30 minutos\n🔥 Audios + fotos + videos calientes\n😈 Tú mandas... yo me entrego\n📲 Todo por chat íntimo\n➡️ Escríbeme: @ami_pra",
        "boton": "💋 Sex Chat"
    },
    "Novia Virtual": {
        "descripcion": "❤️‍🔥 *Novia Virtual* — $500 MXN / 2 semanas\n💌 Trato de novio 24/7\n📱 Mensajes, llamadas, contenido personalizado\n🥺 Te cuido, te caliento, te provoco…\n➡️ Escríbeme: @ami_pra",
        "boton": "❤️‍🔥 Novia Virtual"
    },
    "Video Personalizado": {
        "descripcion": "🎬 *Video Personalizado* — $500 MXN\n⏱️ 20 minutos haciendo lo que tú digas\n🎭 Desinhibida, obediente y entregada\n📦 Entrega < 12 hrs\n🎁 Incluye 15 días *GRATIS* en Canal VIP\n➡️ Escríbeme: @ami_pra",
        "boton": "🎬 Video Personalizado"
    },
    "Sextape": {
        "descripcion": "📹 *Sextape Privada*\n🔥 Videos XXX de 15 a 30 minutos\n👀 Solo para tus ojos\n🧨 Hechos a tu medida\n➡️ Escríbeme: @ami_pra",
        "boton": "📹 Sextape"
    }
}

# Mensaje de bienvenida
def obtener_teclado_servicios():
    botones = [[InlineKeyboardButton(s["boton"], callback_data=key)] for key, s in SERVICIOS.items()]
    return InlineKeyboardMarkup(botones)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bienvenida = "Hola amor... soy *Amanda* 😈\n¿Quieres algo rico, privado y solo para ti? Tengo varios pecados que no se dicen... *se pagan* 🔥\n\nElige el que más se te antoje 👇"
    await update.message.reply_text(bienvenida, parse_mode="Markdown", reply_markup=obtener_teclado_servicios())

# IA para responder mensajes
async def responder_con_ia(mensaje_usuario):
    prompt_base = """
Eres Amanda, una chica erótica, traviesa y cariñosa que vende contenido y servicios íntimos. Usa un tono sexy y atrevido. Si el cliente menciona un servicio específico, responde con la descripción adecuada.

Servicios disponibles:
""" + "\n".join([f"- {k}: {v['descripcion']}" for k,v in SERVICIOS.items()]) + """

Cliente: """ + mensaje_usuario + """
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
