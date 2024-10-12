import pytest
from database.queries import get_user, execute_query
from tests.conftest import create_user

@pytest.mark.asyncio
async def test_update_user():
    # Добавляем пользователя
    await create_user('testuser', 123456)
    user_before = await get_user('testuser')
    assert user_before['role'] == 'user', "Начальное значение роли должно быть 'user'"

    # Обновляем роль пользователя напрямую через SQL
    await execute_query("UPDATE users SET role = 'admin' WHERE username = ?", ('testuser',))

    # Получаем обновленного пользователя
    user_after = await get_user('testuser')
    assert user_after['role'] == 'admin', "Роль должна быть обновлена на 'admin'"
