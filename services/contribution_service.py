# services/contribution_service.py

from database.queries import get_all_contributions, get_contributions, add_contribution as add_contribution_query
import logging

async def get_all_contributions_service(db):
    try:
        contributions = await get_all_contributions(db)
        if contributions:
            contribution_details = "\n".join(
                [f"Пользователь: {c['username']}, Сумма: {c['amount']}, Дата: {c['date']}" for c in contributions]
            )
            return contribution_details
        else:
            return "Нет зарегистрированных взносов."
    except Exception as e:
        logging.error(f"Ошибка при получении взносов: {e}")
        return "Ошибка при получении взносов. Попробуйте позже."

async def add_contribution_service(user_id, amount, date, db):
    try:
        await add_contribution_query(user_id, amount, date, db)
        return f"Взнос {amount} успешно добавлен!"
    except Exception as e:
        logging.error(f"Ошибка при добавлении взноса: {e}")
        return "Ошибка при добавлении взноса. Пожалуйста, попробуйте позже."

async def get_user_contributions_service(user_id, db):
    try:
        contributions = await get_contributions(user_id, db)
        if contributions:
            contribution_details = "\n".join(
                [f"Дата: {c['date']}, Сумма: {c['amount']}" for c in contributions]
            )
            return contribution_details
        else:
            return "Нет зарегистрированных взносов."
    except Exception as e:
        logging.error(f"Ошибка при получении взносов пользователя: {e}")
        return "Ошибка при получении данных о взносах. Пожалуйста, попробуйте позже."
