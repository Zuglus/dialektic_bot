# database/queries.py

import aiosqlite
import config.config as config  # Используем путь к базе данных из конфига

# Инициализация базы данных
async def init_db():
    await execute_query('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    await execute_query('''
        CREATE TABLE IF NOT EXISTS contributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

# Выполнение запроса к базе данных
async def execute_query(query, params=None):
    async with aiosqlite.connect(config.DB_PATH) as db:
        if params:
            await db.execute(query, params)
        else:
            await db.execute(query)
        await db.commit()

# Получение информации о пользователе
async def get_user(username):
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('SELECT id, username, chat_id, role, created_at, updated_at FROM users WHERE username = ?', (username,))
        return await cursor.fetchone()

# Добавление нового пользователя
async def add_user(username, chat_id):
    await execute_query('INSERT INTO users (username, chat_id) VALUES (?, ?)', (username, chat_id))

# Получение всех взносов пользователя
async def get_contributions(user_id):
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('SELECT amount, date FROM contributions WHERE user_id = ?', (user_id,))
        return await cursor.fetchall()

# Получение всех взносов
async def get_all_contributions():
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('''
            SELECT users.username, contributions.amount, contributions.date
            FROM contributions
            JOIN users ON contributions.user_id = users.id
        ''')
        return await cursor.fetchall()
