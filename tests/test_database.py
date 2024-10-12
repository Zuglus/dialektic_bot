# tests/test_database.py
import pytest
from database.models import Database
from database.queries import add_user, get_user

@pytest.mark.asyncio
async def test_add_and_update_user():
    db = Database(db_path=':memory:')
    
    # Инициализация базы данных
    await db.init_db()

    # Проверяем, что таблица users создана
    tables = await db.fetchone("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert tables is not None, "Таблица users должна быть создана"

    # Добавляем нового пользователя
    await add_user('testuser', 123456)

    # Получаем пользователя и проверяем дату создания
    user = await get_user('testuser')
    assert user is not None, "Пользователь должен быть добавлен"
    created_at = user[2]  # Поле даты создания через индекс
    assert created_at is not None

    # Обновляем роль пользователя
    await db.execute("UPDATE users SET role = 'admin' WHERE username = ?", ('testuser',))

    # Проверяем, что поле updated_at изменилось
    user_after_update = await get_user('testuser')
    assert user_after_update[3] != created_at, "Поле updated_at должно быть обновлено при изменении данных пользователя"
