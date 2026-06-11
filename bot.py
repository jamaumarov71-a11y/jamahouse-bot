import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "8825490054:AAE_XQDAVJkssiJ31LKOFDr4BmGq8Tq2v_g"
CHANNEL = "@jamahouse"

# ---------------- OLX PARSER ----------------
def parse_olx(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.text if soup.title else "OLX объявление"

    image = None
    img_tag = soup.find("img")
    if img_tag and img_tag.get("src"):
        image = img_tag["src"]

    return title, image

# ---------------- IMAGE PROCESS ----------------
def crop_image(url):
    r = requests.get(url)
    img = Image.open(BytesIO(r.content))

    width, height = img.size
    img = img.crop((0, 0, width, int(height * 0.85)))

    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer

# ---------------- HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправь OLX ссылку 📦")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "olx" in text:
        title, image = parse_olx(text)

        context.user_data["title"] = title
        context.user_data["image"] = image

        keyboard = [
            [InlineKeyboardButton("📢 Опубликовать", callback_data="publish")]
        ]

        await update.message.reply_text(
            f"📦 Готово:\n\n{title}\n\nНажми кнопку чтобы опубликовать",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("Пришли OLX ссылку")

async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    title = context.user_data.get("title", "OLX")
    image = context.user_data.get("image")

    caption = f"📦 {title}\n\n👉 @jamahouse"

    if image:
        img = crop_image(image)
        await context.bot.send_photo(chat_id=CHANNEL, photo=img, caption=caption)
    else:
        await context.bot.send_message(chat_id=CHANNEL, text=caption)

    await query.edit_message_text("✅ Опубликовано в канал!")

# ---------------- APP ----------------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(CallbackQueryHandler(publish))

print("Bot started")
app.run_polling(drop_pending_updates=True)
