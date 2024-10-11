# tests/test_database.py

import pytest
from database.models import Database
from database.queries import add_user, get_user

@pytest.mark.asyncio
async def test_add_and_get_user():
    db = Database(db_path=':memory:')
    
    # Создаем таблицу перед тестом
    await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')

    # Добавляем пользователя
    await add_user('testuser', 123456)
    
    # Проверяем, что пользователь добавлен
    user = await get_user('testuser')
    assert user is not None
    assert user[1] == 'user'  # Проверяем роль
