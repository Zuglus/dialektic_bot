# database/models.py
import aiosqlite
import logging


class Database:
    def __init__(self, db_path='bot_data.db'):
        self.db_path = db_path

    async def execute(self, query, params=None):
        try:
            async with aiosqlite.connect(self.db_path) as db:
                if params:
                    await db.execute(query, params)
                else:
                    await db.execute(query)
                await db.commit()
        except aiosqlite.Error as e:
            logging.error(f"Database error: {e}")
            raise

    # Инициализация базы данных
    async def init_db():
        db = Database()
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                chat_id INTEGER NOT NULL,
                role TEXT DEFAULT 'user'
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS contributions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

    async def fetchone(self, query, params=None):
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(query, params) if params else await db.execute(query)
                return await cursor.fetchone()
        except aiosqlite.Error as e:
            logging.error(f"Database error: {e}")
            raise
