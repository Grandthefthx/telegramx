import asyncio
import sys
from config import TOKEN
from handlers.start_handler import start
from handlers.article_handler import send_first_article
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# ✅ Если Windows — патчим event loop
if sys.platform == "win32":
    import nest_asyncio
    nest_asyncio.apply()

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # Обработчик команды /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_first_article))  # Обработчик текстов

    print("Бот запущен! 🚀")
    await app.run_polling()

# ✅ Создаём event loop вручную (чтобы работало везде)
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())