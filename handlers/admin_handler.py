from telegram import Update
from telegram.ext import CallbackContext
from database import get_user_role

async def admin_panel(update: Update, context: CallbackContext):
    """Команда доступна только админам"""
    user_id = update.effective_user.id
    role = get_user_role(user_id)

    if role == "admin":
        await update.message.reply_text("🔧 Добро пожаловать в админ-панель!")
    else:
        await update.message.reply_text("🚫 У тебя нет доступа к этой команде.")
