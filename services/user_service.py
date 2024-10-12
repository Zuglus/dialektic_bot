# services/user_service.py

from database.queries import get_user, add_user, get_all_users as fetch_all_users
import logging

async def register_user(username, chat_id, db):
    try:
        existing_user = await get_user(username, db)
        if existing_user:
            return "Пользователь уже зарегистрирован."
        await add_user(username, chat_id, db)
        return f"Пользователь {username} зарегистрирован!"
    except Exception as e:
        logging.error(f"Ошибка при регистрации пользователя: {e}")
        return "Ошибка при регистрации. Попробуйте позже."

async def get_user_info(username, db):
    try:
        user = await get_user(username, db)
        if user:
            return user
        return None
    except Exception as e:
        logging.error(f"Ошибка при получении данных пользователя: {e}")
        return None

async def get_all_users_service(db):
    try:
        return await fetch_all_users(db)
    except Exception as e:
        logging.error(f"Ошибка при получении списка пользователей: {e}")
        return []
