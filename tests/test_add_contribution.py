# tests/test_add_contribution.py

import pytest
from database.queries import get_user, get_contributions
from tests.conftest import create_user, create_contribution

@pytest.mark.asyncio
async def test_add_contribution():
    # Добавляем пользователя
    await create_user('testuser', 123456)
    user = await get_user('testuser')
    user_id = user['id']

    # Добавляем взнос
    await create_contribution(user_id, 100.50, '2024-10-10')

    # Получаем взносы пользователя
    contributions = await get_contributions(user_id)

    # Проверяем корректность добавленного взноса
    assert len(contributions) == 1, "Должен быть один взнос"
    assert contributions[0]['amount'] == 100.50, "Сумма взноса должна совпадать"
    assert contributions[0]['date'] == '2024-10-10', "Дата взноса должна совпадать"
