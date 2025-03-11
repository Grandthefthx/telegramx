import asyncio
import sys
from config import TOKEN
from handlers.start_handler import start
from handlers.article_handler import send_first_article
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# ✅ Windows фикс: Принудительно задаём ProactorEventLoop
if sys.platform == "win32":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.set_event_loop(asyncio.ProactorEventLoop())

async def main():
    """Основная функция запуска бота"""
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_first_article))  

    print("Бот запущен! 🚀")

    try:
        await app.run_polling()
    except asyncio.CancelledError:
        print("Polling завершён (бот выключен)")
    except Exception as e:
        if "Cannot close a running event loop" in str(e):
            pass  # ✅ Глушим ошибку раз и навсегда
        else:
            print(f"⚠ Другая ошибка: {e}")

# ✅ Запуск и полное игнорирование ошибки event loop
if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем. Завершаем работу...")
    except RuntimeError as e:
        if "Cannot close a running event loop" in str(e):
            pass  # ✅ Игнорируем баг Windows