import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "telegram_bot.db")  # Гарантированно создаст в текущей папке

def get_connection():
    """Создаёт и возвращает подключение к базе данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Читаем строки как словарь
    return conn

def init_db():
    """Создаёт таблицу пользователей"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE IF EXISTS users;""")  # Если тестируешь — пересоздаём
    conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        name TEXT
    );
    """)

    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

def add_user(telegram_id, name):
    """Добавляет пользователя в БД или обновляет имя"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET name = ? WHERE telegram_id = ?", (name, telegram_id))
    else:
        cursor.execute("INSERT INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))

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

# ✅ Теперь при запуске database.py создаётся БД
if __name__ == "__main__":
    print(f"📂 База создаётся в: {DB_PATH}")
    init_db()
