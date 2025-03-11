from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters
from database import add_user, get_user_name

# Состояния для диалога
ASK_NAME = 1

async def ask_name(update: Update, context: CallbackContext):
    """Запрашивает имя у нового пользователя"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"

    existing_name = get_user_name(user_id)

    if existing_name:
        # Если пользователь уже есть, просто показываем кнопку
        keyboard = [["✍ Написать Ченеллеру"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Добро пожаловать!", reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        # Если нового пользователя нет в БД, запрашиваем имя
        await update.message.reply_text("Привет, как тебя зовут?")
        return ASK_NAME

async def save_name(update: Update, context: CallbackContext):
    """Сохраняет имя пользователя и завершает диалог"""
    user_id = update.effective_user.id
    name = update.message.text.strip()

    add_user(user_id, name)  # Добавляем в БД

    await update.message.reply_text(f"Приятно познакомиться, {name}!")

    # Показываем кнопку после регистрации
    keyboard = [["✍ Написать Ченеллеру"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Теперь можешь написать Ченеллеру.", reply_markup=reply_markup)

    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    """Выход из диалога, если нужно"""
    await update.message.reply_text("Ок, если передумаешь, просто напиши мне своё имя.")
    return ConversationHandler.END

# Определение диалогового обработчика
start_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.ALL, ask_name)],
    states={ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_name)]},
    fallbacks=[MessageHandler(filters.COMMAND, cancel)]
)