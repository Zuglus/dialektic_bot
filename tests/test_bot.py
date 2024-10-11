import datetime
import unittest
from aiogram import types
from unittest.mock import AsyncMock, patch
from app.handlers import send_welcome
from app.keyboards import main_keyboard  # Импортируем корректную клавиатуру

class TestBotHandlers(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.bot = AsyncMock()  # Мокаем бота

    @patch('aiogram.types.Message.answer', new_callable=AsyncMock)
    async def test_send_welcome(self, mock_answer):
        # Создаем тестовое сообщение
        message = types.Message(
            message_id=1,
            date=datetime.datetime.now(),
            chat=types.Chat(id=123456, type='private'),
            from_user=types.User(id=123456, is_bot=False, first_name='Test', username='testuser'),
            text='/start'
        ).as_(self.bot)  # Привязываем мок-бот к сообщению

        # Вызываем тестируемую функцию
        await send_welcome(message)

        # Проверяем, что message.answer был вызван с нужными аргументами
        mock_answer.assert_called_with(
            "*Привет!* Я бот для учета взносов. Что хотите сделать?",
            reply_markup=main_keyboard(),  # Используем правильную клавиатуру
            parse_mode="Markdown"
        )

if __name__ == '__main__':
    unittest.main()
