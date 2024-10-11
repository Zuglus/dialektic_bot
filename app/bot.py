# app/bot.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import config.config as config
from app.handlers import (
    my_account,
    send_welcome,
    register_user,
    contribute,  # Обновлено с contribute_prompt на contribute
    cancel_contribute,
    process_contribution,
    view_all_contributions,
    view_contributions,
    set_role,
    back_to_main_menu,
    setup_handlers
)
from app.states import ContributionState
from database.models import init_db

bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


def setup_handlers(dp: Dispatcher):
    # Добавляем обработчик команды /start
    dp.message(Command('start'))(send_welcome)
    dp.message(lambda message: message.text == "Назначить роль")(set_role)
    dp.message(lambda message: message.text ==
               "Просмотреть все взносы")(view_all_contributions)
    dp.message(lambda message: message.text ==
               "Зарегистрироваться")(register_user)
    dp.message(lambda message: message.text ==
               "Добавить взнос")(contribute)  # Обновлено
    dp.message(lambda message: message.text == "Отмена")(cancel_contribute)
    dp.message(lambda message: message.text == "Личный кабинет")(my_account)
    dp.message(lambda message: message.text == "Назад в главное меню")(
        back_to_main_menu)  # Добавлен обработчик
    dp.message(ContributionState.waiting_for_amount)(process_contribution)

    # Регистрируем обработчики инлайн-кнопок для личного кабинета
    dp.callback_query(lambda callback: callback.data ==
                      "view_contributions")(view_contributions)


# Настройка обработчиков
setup_handlers(dp)
