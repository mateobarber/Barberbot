from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os

TOKEN = "8840900599:AAFdM48I7eTpf2RmWPwwTnaQFnprHrmbSkA"

ARCHIVO = "datos.json"

def cargar_datos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return {
        "caja": 0,
        "deuda_leo": 1500000
    }

def guardar_datos():
    with open(ARCHIVO, "w") as f:
        json.dump(datos, f)

datos = cargar_datos()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💈 BarberBot Finanzas listo.\n\n"
        "Usa:\n"
        "+25000 corte\n"
        "-10000 comida\n"
        "pagar leo 100000\n"
        "resumen"
    )

async def mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    if texto.startswith("+"):
        valor = int(texto.split()[0][1:])
        datos["caja"] += valor
        guardar_datos()
        await update.message.reply_text(
            f"✅ Ingreso: ${valor:,}\n💰 Caja: ${datos['caja']:,}"
        )

    elif texto.startswith("-"):
        valor = int(texto.split()[0][1:])
        datos["caja"] -= valor
        guardar_datos()
        await update.message.reply_text(
            f"✅ Gasto: ${valor:,}\n💰 Caja: ${datos['caja']:,}"
        )

    elif texto.startswith("pagar leo"):
        valor = int(texto.split()[2])
        datos["deuda_leo"] -= valor
        guardar_datos()
        await update.message.reply_text(
            f"✅ Abono Leo: ${valor:,}\n"
            f"💳 Deuda pendiente: ${datos['deuda_leo']:,}"
        )

    elif texto == "resumen":
        await update.message.reply_text(
            f"📊 Resumen\n\n"
            f"💰 Caja: ${datos['caja']:,}\n"
            f"💳 Deuda Leo: ${datos['deuda_leo']:,}"
        )

    else:
        await update.message.reply_text("No entendí 😅")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensajes))

print("BarberBot con memoria encendido...")
app.run_polling()