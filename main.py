# main.py
import asyncio
from app.bot import dp, bot, init_db  # Импортируем из app.bot

async def main():
    await init_db()  # Инициализация базы данных
    await dp.start_polling(bot)  # Запуск поллинга для обработки сообщений

if __name__ == '__main__':
    asyncio.run(main())
