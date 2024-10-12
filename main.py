# main.py
import asyncio
from app.bot import dp, bot
from database.models import init_db  # Импортируем функцию для инициализации базы данных

async def main():
    await init_db()  # Инициализируем базу данных через чистую функцию
    await dp.start_polling(bot)  # Запуск поллинга для обработки сообщений

if __name__ == '__main__':
    asyncio.run(main())
