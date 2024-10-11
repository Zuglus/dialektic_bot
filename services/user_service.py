# services/user_service.py
from database.queries import get_user, add_user, Database
import logging


class UserService:
    @staticmethod
    async def register_user(username, chat_id):
        try:
            existing_user = await get_user(username)
            if existing_user:
                return "Пользователь уже зарегистрирован."
            await add_user(username, chat_id)
            return f"Пользователь {username} зарегистрирован!"
        except Exception as e:
            logging.error(f"Ошибка при регистрации пользователя: {e}")
            return "Ошибка при регистрации. Попробуйте позже."

    @staticmethod
    async def get_user_info(username):
        try:
            user = await get_user(username)
            if user:
                return user
            return None
        except Exception as e:
            logging.error(f"Ошибка при получении данных пользователя: {e}")
            return None

    @staticmethod
    async def get_all_users():
        db = Database()
        return await db.fetchall('SELECT id, username FROM users')
