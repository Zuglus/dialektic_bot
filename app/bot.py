# app/bot.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties  # Импортируем DefaultBotProperties
import config.config as config
from app.handlers import register_handlers
from database.db import init_db

async def main():
    # Настраиваем параметры по умолчанию
    default_properties = DefaultBotProperties(parse_mode='Markdown')

    # Инициализируем бота и диспетчер
    bot = Bot(
        token=config.API_TOKEN,
        default=default_properties  # Используем default с настройками
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Инициализируем базу данных
    await init_db()

    # Регистрируем обработчики
    register_handlers(dp)

    # Запускаем поллинг
    await dp.start_polling(bot)
