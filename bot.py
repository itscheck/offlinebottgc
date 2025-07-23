
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = '8108034371:AAHtup29JJ59vyMfhAzhYLPiDN5VkcyETAw'
ADMIN_ID = 804223902

WELCOME_MESSAGE = """Если бы можно было вернуть время… Что бы ты написал(а)?

Отправь сообщение, которое хотел(а) сказать, но так и не сказал(а).
Пришли его нам — мы анонимно опубликуем его на канале.

Иногда даже невысказанные слова заслуживают быть услышанными."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    print("Текст:", text)
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 Новое анонимное сообщение:

{text}")
    await update.message.reply_text("✅ Сообщение отправлено анонимно!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo = update.message.photo[-1].file_id
    caption = update.message.caption or "🖼 Анонимное фото"
    print("Фото получено")
    await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=caption)
    await update.message.reply_text("✅ Фото отправлено анонимно!")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    voice = update.message.voice.file_id
    print("Голосовое сообщение получено")
    await context.bot.send_voice(chat_id=ADMIN_ID, voice=voice, caption="🎤 Анонимное голосовое сообщение")
    await update.message.reply_text("✅ Голосовое сообщение отправлено анонимно!")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("Бот запущен...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())
