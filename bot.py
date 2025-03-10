from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.start_handler import start
from config import TOKEN
import asyncio
import nest_asyncio  # <-- Добавляем это

nest_asyncio.apply()  # <-- Обязательно для совместимости с VS Code

async def main():
    # Создаем приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Запуск бота
    await app.run_polling()

# Обновляем запуск для совместимости с VS Code
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Если цикл уже запущен (как в VS Code), просто запускаем main
        loop.create_task(main())
    else:
        # Если не запущен, запускаем нормально
        loop.run_until_complete(main())
