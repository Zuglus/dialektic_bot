# tests/test_bot.py

import asyncio
import unittest
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import send_welcome
from unittest.mock import AsyncMock
import datetime

class TestBotHandlers(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.bot = Bot(token="test_token")  # Фиктивный токен
        self.dp = Dispatcher(storage=MemoryStorage())
        
        # Мокируем метод отправки сообщений
        self.bot.send_message = AsyncMock()

    async def test_send_welcome(self):
        message = types.Message(
            message_id=1,
            date=datetime.datetime.now(),
            chat=types.Chat(id=123456, type='private'),
            from_user=types.User(id=123456, is_bot=False, first_name='Test', username='testuser'),
            text='/start'
        ).as_(self.bot)  # Привязываем бот к сообщению

        await send_welcome(message)
        
        # Проверяем, что сообщение отправлено
        self.bot.send_message.assert_called_with(123456, "*Привет!* Я бот для учета взносов. Что хотите сделать?", parse_mode="Markdown")

if __name__ == '__main__':
    unittest.main()
