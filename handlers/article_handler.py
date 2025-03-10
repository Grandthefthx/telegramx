from telegram import Update
from telegram.ext import CallbackContext
from database import get_connection

async def send_first_article(update: Update, context: CallbackContext):
    # Получаем статью с send_after_days = 0 из БД
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM articles WHERE send_after_days = 0")
    article = cursor.fetchone()
    conn.close()

    if article:
        title = article['title']
        content = article['content']
        await update.message.reply_text(f"*{title}*\n\n{content}", parse_mode='Markdown')