# database/models.py

import aiosqlite
import logging
from datetime import datetime
from config.config import DB_PATH  # Импорт пути к базе данных из конфига

async def connect_to_db(db_path=DB_PATH):
    return await aiosqlite.connect(db_path)

async def execute_query(db, query, params=None):
    try:
        logging.info(f"Executing query: {query}, params: {params}")
        if params:
            await db.execute(query, params)
        else:
            await db.execute(query)
        await db.commit()  # Убедимся, что данные фиксируются
    except aiosqlite.Error as e:
        logging.error(f"Database error: {e}")
        raise

async def fetch_one(db, query, params=None):
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(query, params) if params else await db.execute(query)
    return await cursor.fetchone()

async def fetch_all(db, query, params=None):
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(query, params) if params else await db.execute(query)
    return await cursor.fetchall()

async def init_db(db):
    await execute_query(db, '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    await execute_query(db, '''
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
