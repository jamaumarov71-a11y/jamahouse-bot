from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8825490054:AAE_XQDAVJkssiJ31LKOFDr4BmGq8Tq2v_g"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает ✅ Отправь ссылку OLX")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "olx" in text:
        await update.message.reply_text(
            "📦 OLX ссылка получена!\n\n"
            "Скоро добавим:\n"
            "✔ фото\n✔ описание\n✔ кнопка публикации"
        )
    else:
        await update.message.reply_text("Отправь OLX ссылку")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, text_handler))

print("Bot started")
app.run_polling()
