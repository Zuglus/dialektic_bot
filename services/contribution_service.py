# services/contribution_service.py
from database.queries import get_all_contributions, get_contributions, add_contribution
import logging


class ContributionService:
    @staticmethod
    async def get_all_contributions():
        try:
            contributions = await get_all_contributions()
            if contributions:
                contribution_details = "\n".join(
                    [f"Пользователь: {c[0]}, Сумма: {c[1]}, Дата: {
                        c[2]}" for c in contributions]
                )
                return contribution_details
            else:
                return "Нет зарегистрированных взносов."
        except Exception as e:
            logging.error(f"Ошибка при получении взносов: {e}")
            return "Ошибка при получении взносов. Попробуйте позже."

    @staticmethod
    async def add_contribution(user_id, amount, date):
        try:
            await add_contribution(user_id, amount, date)
            return f"Взнос {amount} успешно добавлен!"
        except Exception as e:
            logging.error(f"Ошибка при добавлении взноса: {e}")
            return "Ошибка при добавлении взноса. Пожалуйста, попробуйте позже."

    @staticmethod
    async def get_user_contributions(user_id):
        try:
            contributions = await get_contributions(user_id)
            if contributions:
                contribution_details = "\n".join(
                    [f"Дата: {c[1]}, Сумма: {c[0]}" for c in contributions]
                )
                return contribution_details
            else:
                return "Нет зарегистрированных взносов."
        except Exception as e:
            logging.error(f"Ошибка при получении взносов пользователя: {e}")
            return "Ошибка при получении данных о взносах. Пожалуйста, попробуйте позже."
