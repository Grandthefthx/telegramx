import asyncio
import sys
from config import TOKEN
from handlers.start_handler import start_conversation
from handlers.admin_handler import admin_panel, create_story, list_stories, receive_story, receive_frequency
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

# ✅ Windows фикс: ProactorEventLoop
if sys.platform == "win32":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.set_event_loop(asyncio.ProactorEventLoop())

# ✅ Определяем состояния для диалога создания сториз
ASK_STORY, ASK_FREQUENCY = range(2)

async def main():
    """Запуск бота"""
    app = ApplicationBuilder().token(TOKEN).build()

    # ✅ Команда входа в админ-панель
    app.add_handler(CommandHandler("admin", admin_panel))

    # ✅ Команда просмотра сториз
    app.add_handler(CommandHandler("list_stories", list_stories))

    # ✅ Диалог для создания сториз
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex("Создать стори"), create_story)],
        states={
            ASK_STORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_story)],
            ASK_FREQUENCY: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_frequency)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)

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
