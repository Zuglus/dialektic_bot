# tests/test_user_creation.py

import pytest
from database.queries import get_user
from tests.conftest import create_user

@pytest.mark.asyncio
async def test_add_user():
    # Добавляем пользователя
    await create_user('testuser', 123456)
    user = await get_user('testuser')

    # Проверка данных пользователя
    assert user is not None, "Пользователь должен быть добавлен"
    assert user['username'] == 'testuser', "Имя пользователя должно совпадать"
    assert user['chat_id'] == 123456, "Chat ID должен совпадать"
