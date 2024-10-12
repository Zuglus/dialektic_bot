# database/db.py

import aiosqlite
import logging
from config.config import DB_PATH

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация базы данных
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                chat_id INTEGER NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS contributions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        await db.commit()
        logger.info("База данных успешно инициализирована.")

# Общая функция для выполнения запросов
async def execute_query(query: str, params: tuple = None):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            if params:
                await db.execute(query, params)
            else:
                await db.execute(query)
            await db.commit()
    except Exception as e:
        logger.error(f"Ошибка при выполнении запроса: {e}")
        raise

# Получение информации о пользователе
async def get_user(user_id: int):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            return await cursor.fetchone()
    except Exception as e:
        logger.error(f"Ошибка при получении пользователя: {e}")
        raise

# Добавление нового пользователя
async def add_user(user_id: int, username: str, chat_id: int):
    try:
        await execute_query(
            'INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?)',
            (user_id, username, chat_id)
        )
        logger.info(f"Пользователь {username} добавлен в базу данных.")
    except aiosqlite.IntegrityError:
        logger.warning(f"Пользователь с user_id {user_id} уже существует.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        raise

# Получение всех взносов пользователя
async def get_contributions_by_user(user_id: int):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('SELECT * FROM contributions WHERE user_id = ?', (user_id,))
            return await cursor.fetchall()
    except Exception as e:
        logger.error(f"Ошибка при получении взносов: {e}")
        raise

# Добавление взноса
async def add_contribution(user_id: int, amount: float):
    try:
        await execute_query(
            'INSERT INTO contributions (user_id, amount) VALUES (?, ?)',
            (user_id, amount)
        )
        logger.info(f"Добавлен взнос {amount} от пользователя {user_id}.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении взноса: {e}")
        raise

# Получение всех взносов
async def get_all_contributions():
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('''
                SELECT users.username, contributions.amount, contributions.date
                FROM contributions
                JOIN users ON contributions.user_id = users.user_id
            ''')
            return await cursor.fetchall()
    except Exception as e:
        logger.error(f"Ошибка при получении всех взносов: {e}")
        raise

# Получение всех пользователей
async def get_all_users():
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('SELECT * FROM users')
            return await cursor.fetchall()
    except Exception as e:
        logger.error(f"Ошибка при получении пользователей: {e}")
        raise
