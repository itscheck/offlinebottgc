
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import nest_asyncio

nest_asyncio.apply()

TOKEN = "8108034371:AAHtup29JJ59vyMfhAzhYLPiDN5VkcyETAw"
ADMIN_ID = 804223902  # ✅ целое число, не строка

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

START_TEXT = """📩 Если бы можно было вернуть время… Что бы ты написал(а)?

Отправь сообщение, которое хотел(а) сказать, но так и не сказал(а).
Пришли его нам — мы анонимно опубликуем его на канале.

Иногда даже невысказанные слова заслуживают быть услышанными."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"📨 Новое анонимное сообщение:\n\n{message}")
    await update.message.reply_text("✅ Твоё сообщение отправлено!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1].file_id
    caption = update.message.caption or "(без текста)"
    await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=f"🖼 Анонимное фото:\n\n{caption}")
    await update.message.reply_text("✅ Фото отправлено!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling() 