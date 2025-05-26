import logging
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import openai
from dotenv import load_dotenv

# Carga del entorno
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar OpenAI
openai.api_key = OPENAI_API_KEY

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Memoria de usuarios e interacciones
user_data = {}
PRODUCTO = "🔥 Canal VIP con +200 fotos y videos xxx, mi WhatsApp personal, sexchat o videollamadas. Todo desde 300 MXN. Escríbeme si te animas."

# Precios y link de pago
VENTA = "❤️ Canal VIP: $300\n🎥 Videollamada: $500\n💬 Sex Chat: $300\nPago por Mercado Pago: https://www.mercadopago.com.mx/subscriptions/checkout?preapproval_plan_id=2c93808497030fc701970475adc70044 o transferencia, escríbeme a @ami_pra"

# Generar respuesta corta y directa
async def generar_respuesta(texto):
    prompt = f"Responde como una mujer erótica, muy sugestiva pero con mensajes de máximo 3 renglones. Siempre incluye algo del siguiente producto: '{PRODUCTO}'. Sé directa, habla como si estuvieras en confianza con el usuario, y busca vender.\nUsuario: {texto}\nAmanda:"  

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres Amanda, una asistente erótica que busca vender acceso al canal VIP y servicios."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=100
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error al generar respuesta de OpenAI: {e}")
        return "Algo falló, amor... pero sigo aquí para ti."

# Lógica de conteo por usuario
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    texto = update.message.text

    if user_id not in user_data:
        user_data[user_id] = {"mensajes": 0, "interes": False}

    user_data[user_id]["mensajes"] += 1

    # Detectar intención de compra
    if any(palabra in texto.lower() for palabra in ["precio", "costo", "comprar", "canal", "vip", "pagar"]):
        user_data[user_id]["interes"] = True
        await update.message.reply_text(VENTA)
        return

    if user_data[user_id]["mensajes"] >= 4 and not user_data[user_id]["interes"]:
        await update.message.reply_text("Amor, si no quieres nada rico por ahora... mejor guárdame para después 😘")
        return

    respuesta = await generar_respuesta(texto)
    await update.message.reply_text(respuesta)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hola amor 😘 Soy Amanda. Cuéntame, ¿en qué estábamos?")

def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    app.run_polling()

if __name__ == "__main__":
    main()
