import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "telegram_bot.db")  # Гарантированно создаст в текущей папке

def get_connection():
    """Создаёт и возвращает подключение к базе данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Читаем строки как словарь
    return conn

def init_db():
    """Создаёт таблицы пользователей и сториз"""
    conn = get_connection()
    cursor = conn.cursor()

    # ✅ Пересоздаём таблицы (если тестируешь)
    cursor.execute("DROP TABLE IF EXISTS users;")
    cursor.execute("DROP TABLE IF EXISTS stories;")
    conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        name TEXT,
        role TEXT DEFAULT 'user'
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        frequency INTEGER NOT NULL
    );
    """)

    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

def add_user(telegram_id, name, role="user"):
    """Добавляет пользователя в БД или обновляет его имя"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET name = ? WHERE telegram_id = ?", (name, telegram_id))
    else:
        cursor.execute("INSERT INTO users (telegram_id, name, role) VALUES (?, ?, ?)", (telegram_id, name, role))

    conn.commit()
    conn.close()

def get_user_name(telegram_id):
    """Получает имя пользователя по его Telegram ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    
    conn.close()
    return user["name"] if user else None

def get_user_role(telegram_id):
    """Получает роль пользователя (admin/user)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT role FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    
    conn.close()
    return user["role"] if user else "user"

def add_story(text, frequency):
    """Добавляет сториз в базу"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stories (text, frequency) VALUES (?, ?)", (text, frequency))
    conn.commit()
    story_id = cursor.lastrowid
    conn.close()
    return story_id

def get_stories():
    """Получает список сториз"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, frequency FROM stories")
    stories = cursor.fetchall()
    conn.close()
    
    return [{"id": row["id"], "text": row["text"], "frequency": row["frequency"]} for row in stories]

# ✅ Укажи администраторов
ADMINS = [
    (249554831, "CharlieDarker", "admin"),  # Твой ID
    (987654321, "wife_nickname", "admin")   # ID жены
]

if __name__ == "__main__":
    print(f"📂 База создаётся в: {DB_PATH}")
    init_db()
    for admin in ADMINS:
        add_user(*admin)
    print("✅ Админы добавлены в БД")
