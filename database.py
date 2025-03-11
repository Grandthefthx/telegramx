import json
import sqlite3

DB_PATH = "telegram_bot.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Чтобы работать с именами полей
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Создаем таблицу users (без удаления)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        language_code TEXT,
        subscription_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_message_date DATETIME,
        interaction_count INTEGER DEFAULT 0,
        device_type TEXT,
        time_zone TEXT,
        ip_address TEXT
    );
    """)

    # Создаем таблицу статей (без удаления)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        send_after_days INTEGER NOT NULL
    );
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Загружаем статьи из JSON в БД (без дубликатов)
def load_articles():
    conn = get_connection()
    cursor = conn.cursor()

    # Загружаем статьи из JSON
    with open('data/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # Добавляем статьи, если их еще нет
    for article in articles:
        cursor.execute("""
            INSERT INTO articles (title, content, send_after_days)
            SELECT ?, ?, ? WHERE NOT EXISTS (
                SELECT 1 FROM articles WHERE title = ? AND content = ?
            )
        """, (article['title'], article['content'], article['send_after_days'],
              article['title'], article['content']))

    conn.commit()
    conn.close()
    print("Articles loaded successfully!")

# Выполняем инициализацию базы при запуске скрипта
if __name__ == "__main__":
    init_db()        # Создаем таблицы (без удаления)
    load_articles()  # Загружаем статьи без дублирования