import asyncio
import sys
from config import TOKEN
from handlers.start_handler import start_conversation
from telegram.ext import ApplicationBuilder

# ✅ Windows фикс: ProactorEventLoop
if sys.platform == "win32":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.set_event_loop(asyncio.ProactorEventLoop())

async def main():
    """Запуск бота"""
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(start_conversation)  # Добавляем диалог

    print("Бот запущен! 🚀")
    
    try:
        await app.run_polling()
    except asyncio.CancelledError:
        print("Polling завершён (бот выключен)")
    except Exception as e:
        if "Cannot close a running event loop" in str(e):
            pass
        else:
            print(f"⚠ Другая ошибка: {e}")

if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем.")
    except RuntimeError as e:
        if "Cannot close a running event loop" in str(e):
            pass