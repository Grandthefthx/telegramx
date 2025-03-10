from telegram import Update
from telegram.ext import CallbackContext
from database import get_connection
from handlers.article_handler import send_first_article

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    telegram_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    language_code = user.language_code

    # Сохраняем данные пользователя в БД
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (telegram_id, username, first_name, last_name, language_code)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(telegram_id) DO NOTHING
    """, (telegram_id, username, first_name, last_name, language_code))
    conn.commit()
    conn.close()

    # Приветственное сообщение и первая статья
    await update.message.reply_text(f"Привет, {first_name}! 👋 Сейчас отправлю тебе первую статью.")
    await send_first_article(update, context)
