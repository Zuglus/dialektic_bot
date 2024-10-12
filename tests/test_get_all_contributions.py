# tests/test_get_all_contributions.py

import pytest
from database.queries import get_user, get_all_contributions
from tests.conftest import create_user, create_contribution

@pytest.mark.asyncio
async def test_get_all_contributions():
    # Добавляем пользователей
    await create_user('testuser1', 123456)
    await create_user('testuser2', 789012)

    user1 = await get_user('testuser1')
    user2 = await get_user('testuser2')

    # Добавляем взносы для обоих пользователей
    await create_contribution(user1['id'], 100.50, '2024-10-10')
    await create_contribution(user2['id'], 200.75, '2024-10-11')

    # Получаем все взносы
    all_contributions = await get_all_contributions()

    # Проверяем, что добавлены два взноса
    assert len(all_contributions) == 2, "Должны быть два взноса"

    # Проверяем данные взносов
    assert all_contributions[0]['username'] == 'testuser1', "Имя пользователя должно совпадать"
    assert all_contributions[0]['amount'] == 100.50, "Сумма первого взноса должна совпадать"
    assert all_contributions[0]['date'] == '2024-10-10', "Дата первого взноса должна совпадать"

    assert all_contributions[1]['username'] == 'testuser2', "Имя второго пользователя должно совпадать"
    assert all_contributions[1]['amount'] == 200.75, "Сумма второго взноса должна совпадать"
    assert all_contributions[1]['date'] == '2024-10-11', "Дата второго взноса должна совпадать"
