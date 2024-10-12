# app/handlers.py
import logging
from aiogram import types
from aiogram.fsm.context import FSMContext
from app.keyboards import account_keyboard, cancel_keyboard, generate_user_keyboard, main_keyboard
from services.user_service import get_user_info, register_user_service
from services.contribution_service import get_user_contributions, add_user_contribution, get_all_user_contributions
from app.states import ContributionState


async def send_welcome(message: types.Message):
    await message.answer(
        "*Привет!* Я бот для учета взносов. Что хотите сделать?",
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )


async def register_user(message: types.Message):
    username = message.from_user.username
    chat_id = message.from_user.id
    result_message = await register_user_service(username, chat_id)
    await message.answer(result_message, reply_markup=main_keyboard(), parse_mode="Markdown")


async def my_account(message: types.Message):
    username = message.from_user.username
    user = await get_user_info(username)
    if user:
        await message.answer("Ваш личный кабинет:", reply_markup=account_keyboard())
    else:
        await message.answer("Вы не зарегистрированы. Нажмите 'Зарегистрироваться' для начала.")


async def view_contributions(message: types.Message):
    username = message.from_user.username
    user = await get_user_info(username)

    if user:
        user_id = user[0]
        contribution_details = await get_user_contributions(user_id)
        await message.answer(f"*История взносов:*\n{contribution_details}", parse_mode="Markdown")
    else:
        await message.answer("Вы не зарегистрированы. Нажмите 'Зарегистрироваться' для начала.")


async def process_contribution(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        username = message.from_user.username
        user = await get_user_info(username)

        if user:
            user_id = user[0]
            date = message.date.strftime("%Y-%m-%d %H:%M:%S")
            result_message = await add_user_contribution(user_id, amount, date)
            await message.answer(result_message, reply_markup=main_keyboard())
            await state.clear()
        else:
            await message.answer("Вы не зарегистрированы. Нажмите кнопку 'Зарегистрироваться' для регистрации.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму.")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Ошибка при сохранении взноса. Пожалуйста, попробуйте позже.")


async def contribute(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите сумму взноса или нажмите 'Отмена'.", reply_markup=cancel_keyboard())
    await state.set_state(ContributionState.waiting_for_amount)


async def cancel_contribute(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == ContributionState.waiting_for_amount:
        await state.clear()
        await message.answer("Операция отменена.", reply_markup=main_keyboard())
    else:
        await message.answer("Нечего отменять.", reply_markup=main_keyboard())


async def view_all_contributions(message: types.Message):
    username = message.from_user.username
    user = await get_user_info(username)

    if user and user[1] == 'admin':
        contribution_details = await get_all_user_contributions()
        await message.answer(f"*Все взносы:*\n{contribution_details}", parse_mode="Markdown")
    else:
        await message.answer("У вас нет прав для просмотра всех взносов.")


async def set_role(message: types.Message):
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Использование: введите имя пользователя и роль через пробел, например: Иван admin.")
        return

    username = args[1]
    role = args[2]

    if role not in ['user', 'admin']:
        await message.answer("Неверная роль. Доступные роли: user, admin")
        return

    from_user = message.from_user.username
    user = await get_user_info(from_user)

    if user and user[1] != 'admin':
        await message.answer("У вас нет прав для назначения ролей.")
        return

    try:
        await update_user_role(username, role)  # Используем сервис для обновления роли
        await message.answer(f"Роль пользователя {username} изменена на {role}.")
    except Exception as e:
        logging.error(f"Ошибка при назначении роли: {e}")
        await message.answer("Ошибка при назначении роли. Пожалуйста, попробуйте позже.")


async def back_to_main_menu(message: types.Message):
    await message.answer("Возвращаемся в главное меню.", reply_markup=main_keyboard())


async def change_page(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split(':')[1])
    keyboard = await generate_user_keyboard(page=page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)


async def select_user(callback_query: types.CallbackQuery):
    username = callback_query.data.split(':')[1]
    await callback_query.message.answer(f"Вы выбрали пользователя: {username}. Теперь выберите роль.")
    keyboard = await generate_role_keyboard(username)
    await callback_query.message.answer("Выберите роль:", reply_markup=keyboard)


async def generate_role_keyboard(username):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(
        text="admin", callback_data=f"set_role:{username}:admin"))
    keyboard.add(InlineKeyboardButton(
        text="user", callback_data=f"set_role:{username}:user"))
    return keyboard


async def set_role_callback(callback_query: types.CallbackQuery):
    data = callback_query.data.split(':')
    username = data[1]
    role = data[2]

    from_user = callback_query.from_user.username
    user = await get_user_info(from_user)

    if user and user[1] != 'admin':
        await callback_query.message.answer("У вас нет прав для назначения ролей.")
        return

    try:
        await update_user_role(username, role)
        await callback_query.message.answer(f"Роль пользователя {username} успешно изменена на {role}.")
    except Exception as e:
        logging.error(f"Ошибка при назначении роли: {e}")
        await callback_query.message.answer("Ошибка при назначении роли. Пожалуйста, попробуйте позже.")


def setup_handlers(dp):
    dp.callback_query_handler(
        lambda callback: callback.data.startswith('page'))(change_page)
    dp.callback_query_handler(
        lambda callback: callback.data.startswith('select_user'))(select_user)
    dp.callback_query_handler(
        lambda callback: callback.data.startswith('set_role'))(set_role_callback)
