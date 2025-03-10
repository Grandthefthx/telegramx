# 🤖 Telegram Bot — Статьи по расписанию

### 📋 Описание
Этот Telegram-бот отправляет статьи пользователям по расписанию после подписки.  
- 📥 Спрашивает имя при первом запуске.  
- 🗂 Сохраняет данные пользователя в SQLite.  
- 📅 Отправляет статьи по заданному расписанию.  
- 🔄 Легко настраиваемые статьи через БД (`articles` таблица).  

---

### 📁 Структура проекта
```
telegramx/
├── bot.py                # Основной файл запуска бота
├── config.py             # Конфигурации и токен бота
├── database.py           # Создание и работа с БД
├── requirements.txt      # Зависимости
├── README.md             # Этот файл
├── .env                  # Токен бота и переменные среды
├── data/
│   ├── articles.json     # Статьи для загрузки в БД
├── handlers/
│   ├── start_handler.py  # Обработчик команды /start
│   ├── article_handler.py # Отправка статей пользователю
├── venv/                 # Виртуальное окружение
```

---

### ⚙️ Установка
1. Клонируем репозиторий и переходим в папку:
   ```bash
   git clone https://github.com/твой_репозиторий/telegramx.git
   cd telegramx
   ```

2. Создаем виртуальное окружение и активируем:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Устанавливаем зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создаем файл `.env` и вставляем токен:
   ```
   TELEGRAM_BOT_TOKEN=твой_токен_здесь
   ```

5. Инициализируем БД и загружаем статьи:
   ```bash
   python database.py
   ```

---

### 🚀 Запуск бота
```bash
python bot.py
```

---

### 🛠 Настройка статей
- Формат статей в `data/articles.json`:
   ```json
   [
       {"title": "Статья 1", "content": "Это первая статья.", "send_after_days": 0},
       {"title": "Статья 2", "content": "Это вторая статья.", "send_after_days": 2}
   ]
   ```

- Добавление новых статей:
   1. Обнови `articles.json`.  
   2. Перезапусти `database.py`:
      ```bash
      python database.py
      ```

---

### 📦 Зависимости (`requirements.txt`)
```
python-telegram-bot>=20.0
python-dotenv
APScheduler
```

---

### 🛡 Возможные ошибки и решения
1. **Ошибка: `This event loop is already running`**
   - Причина: VS Code использует свой `event loop`.
   - Решение: Добавлен `nest_asyncio` для совместимости.

2. **Ошибка: `ON CONFLICT clause does not match`**
   - Причина: `telegram_id` не был `UNIQUE`.
   - Решение: Пересоздали таблицу `users` с `UNIQUE`.

---

### 🛠 Автозапуск на сервере
1. Скрипт `start_bot.sh`:
   ```bash
   #!/bin/bash
   source venv/bin/activate
   nohup python bot.py > bot.log 2>&1 &
   ```

2. Автозапуск через `crontab`:
   ```bash
   @reboot /path/to/telegramx/start_bot.sh
   ```

---

### 🖥 Технологии
- **Язык:** Python 3.10+  
- **Библиотеки:** `python-telegram-bot`, `APScheduler`, `sqlite3`  
- **БД:** SQLite (локальная база данных)  

---

### 📞 Контакты
- **Автор:** Илья  
- **Telegram:** [@твой_ник](https://t.me/твой_ник)  
- **GitHub:** [твой_репозиторий](https://github.com/твой_репозиторий)

---

🔥 **Готово! Если будут вопросы — пиши!** 😎
