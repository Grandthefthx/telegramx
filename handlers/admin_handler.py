from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from database import add_story, get_stories, get_user_role

# ✅ Определяем состояния
ASK_STORY, ASK_FREQUENCY = range(2)

async def admin_panel(update: Update, context: CallbackContext):
    """Команда доступна только админам"""
    user_id = update.effective_user.id
    role = get_user_role(user_id)

    if role != "admin":
        await update.message.reply_text("🚫 У тебя нет доступа к этой команде.")
        return

    keyboard = [["Создать стори", "Посмотреть стори"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("🔧 Админ-панель", reply_markup=reply_markup)

async def create_story(update: Update, context: CallbackContext):
    """Начало процесса создания стори"""
    await update.message.reply_text("✏ Вставь её сюда скорее!")
    return ASK_STORY

async def receive_story(update: Update, context: CallbackContext):
    """Получение текста стори"""
    context.user_data["story"] = update.message.text
    await update.message.reply_text("📩 Напиши как часто шлем (в часах)")
    return ASK_FREQUENCY

async def receive_frequency(update: Update, context: CallbackContext):
    """Получение частоты рассылки"""
    frequency = update.message.text
    if not frequency.isdigit():
        await update.message.reply_text("⛔ Введи число (кол-во часов). Попробуй снова.")
        return ASK_FREQUENCY

    frequency = int(frequency)
    story_text = context.user_data["story"]

    # ✅ Добавляем в БД
    story_id = add_story(story_text, frequency)

    await update.message.reply_text(f"✅ Стори #{story_id} добавлена!\nЧастота: {frequency} часов")
    return ConversationHandler.END

async def list_stories(update: Update, context: CallbackContext):
    """Вывод списка сториз"""
    stories = get_stories()

    if not stories:
        await update.message.reply_text("📭 Пока нет сториз.")
        return

    message = "📜 Список сториз:\n"
    for story in stories:
        message += f"{story['id']} - {' '.join(story['text'].split()[:4])}... - {story['frequency']}ч\n"

    await update.message.reply_text(message)
