# main.py
import asyncio
from app.bot import dp, bot
from database.models import Database  # Импортируем класс Database

async def main():
    db = Database()  # Создаем экземпляр Database
    await db.init_db()  # Инициализируем базу данных через экземпляр
    await dp.start_polling(bot)  # Запуск поллинга для обработки сообщений

if __name__ == '__main__':
    asyncio.run(main())
