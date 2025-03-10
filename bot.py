import asyncio
import nest_asyncio
from config import TOKEN
from handlers.start_handler import start
from handlers.article_handler import send_first_article
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Патчим event loop для совместимости с Docker
nest_asyncio.apply()

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # Обработчик команды /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_first_article))  # Обработчик текстовых сообщений

    print("Бот запущен в Docker! 🚀")
    await app.run_polling()

# Запускаем main без loop.close()
asyncio.run(main())