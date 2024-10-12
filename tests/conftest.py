import pytest_asyncio
from database.queries import init_db, execute_query
from config.config import TEST_DB_PATH
from tests.utils import remove_test_db

# Фикстура для очистки и инициализации базы данных перед каждым тестом
@pytest_asyncio.fixture(autouse=True)
async def cleanup_db():
    remove_test_db()  # Удаляем тестовую базу данных
    await init_db()  # Инициализация базы данных после очистки
    await execute_query("DELETE FROM users")
    await execute_query("DELETE FROM contributions")

# Вспомогательная функция для добавления пользователя
async def create_user(username, chat_id):
    await execute_query('INSERT INTO users (username, chat_id) VALUES (?, ?)', (username, chat_id))

# Вспомогательная функция для добавления взноса
async def create_contribution(user_id, amount, date):
    await execute_query('INSERT INTO contributions (user_id, amount, date) VALUES (?, ?, ?)', (user_id, amount, date))
