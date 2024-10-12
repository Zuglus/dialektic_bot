# app/handlers.py

import logging
from aiogram import types, Router, Dispatcher, F
from aiogram.types import CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from app.keyboards import (
    main_inline_keyboard,
    cancel_inline_keyboard,
    account_inline_keyboard,
    confirm_inline_keyboard,
    generate_user_keyboard
)
from app.states import (
    WAITING_FOR_AMOUNT,
    WAITING_FOR_CONFIRMATION
)
from database.db import (
    add_user,
    get_user,
    add_contribution,
    get_contributions_by_user,
    get_all_contributions,
    get_all_users
)

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем роутер
router = Router()


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    """Приветственное сообщение с основным меню."""
    try:
        await message.answer(
            "Добро пожаловать! Выберите действие:",
            reply_markup=main_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка в send_welcome: {e}")


@router.callback_query(F.data == 'register_user')
async def register_user(callback_query: CallbackQuery):
    """Регистрация нового пользователя."""
    try:
        user = callback_query.from_user
        if await get_user(user.id):
            await callback_query.answer("Вы уже зарегистрированы.", show_alert=True)
        else:
            await add_user(user.id, user.full_name, callback_query.message.chat.id)
            await callback_query.answer("Вы успешно зарегистрированы!")
        await callback_query.message.delete()
    except Exception as e:
        logger.error(f"Ошибка в register_user: {e}")


@router.callback_query(F.data == 'contribute')
async def contribute(callback_query: CallbackQuery, state: FSMContext):
    """Начало процесса добавления взноса."""
    try:
        await callback_query.message.delete()
        await callback_query.message.answer(
            "Введите сумму взноса:",
            reply_markup=cancel_inline_keyboard()
        )
        await state.set_state(WAITING_FOR_AMOUNT)
    except Exception as e:
        logger.error(f"Ошибка в contribute: {e}")


@router.message(StateFilter(WAITING_FOR_AMOUNT))
async def process_contribution(message: types.Message, state: FSMContext):
    """Обработка введенной суммы взноса."""
    try:
        amount_text = message.text.replace(',', '.')
        amount = float(amount_text)
        await state.update_data(amount=amount)
        await message.answer(
            f"Вы ввели сумму *{amount}* у.е. Подтвердить?",
            reply_markup=confirm_inline_keyboard(),
            parse_mode='Markdown'
        )
        await state.set_state(WAITING_FOR_CONFIRMATION)
    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму.")
    except Exception as e:
        logger.error(f"Ошибка в process_contribution: {e}")
        await message.answer("Произошла ошибка при обработке суммы.")
        await state.clear()


@router.callback_query(StateFilter(WAITING_FOR_CONFIRMATION), F.data == 'confirm_contribution')
async def confirm_contribution(callback_query: CallbackQuery, state: FSMContext):
    """Подтверждение взноса и сохранение в базе данных."""
    try:
        data = await state.get_data()
        amount = data.get('amount')
        user_id = callback_query.from_user.id
        await add_contribution(user_id, amount)
        await callback_query.answer("Взнос успешно добавлен!")
        await callback_query.message.delete()
        await callback_query.message.answer(
            "Спасибо за ваш взнос!",
            reply_markup=main_inline_keyboard()
        )
        await state.clear()
    except Exception as e:
        logger.error(f"Ошибка в confirm_contribution: {e}")
        await callback_query.message.answer("Произошла ошибка при добавлении взноса.")
        await state.clear()


@router.callback_query(StateFilter('*'), F.data.in_(['cancel', 'cancel_contribution']))
async def cancel_contribution(callback_query: CallbackQuery, state: FSMContext):
    """Отмена процесса добавления взноса."""
    try:
        await state.clear()
        await callback_query.answer("Действие отменено.")
        await callback_query.message.delete()
        await send_welcome(callback_query.message)
    except Exception as e:
        logger.error(f"Ошибка в cancel_contribution: {e}")


@router.callback_query(F.data == 'my_account')
async def my_account(callback_query: CallbackQuery):
    """Отображение личного кабинета пользователя."""
    try:
        user = await get_user(callback_query.from_user.id)
        if user:
            await callback_query.message.delete()
            await callback_query.message.answer(
                f"Личный кабинет: {user['username']}",
                reply_markup=account_inline_keyboard()
            )
        else:
            await callback_query.answer("Вы не зарегистрированы.", show_alert=True)
    except Exception as e:
        logger.error(f"Ошибка в my_account: {e}")


@router.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(callback_query: CallbackQuery):
    """Возврат в главное меню."""
    try:
        await callback_query.message.delete()
        await send_welcome(callback_query.message)
    except Exception as e:
        logger.error(f"Ошибка в back_to_main_menu: {e}")


@router.callback_query(F.data == 'view_contributions')
async def view_contributions(callback_query: CallbackQuery):
    """Просмотр взносов пользователя."""
    try:
        contributions = await get_contributions_by_user(callback_query.from_user.id)
        if contributions:
            total = sum([c['amount'] for c in contributions])
            message_text = f"Ваши взносы:\nОбщая сумма: *{total}* у.е.\n"
            for c in contributions:
                date = c['date'].split(' ')[0]
                message_text += f"- {c['amount']} у.е. от {date}\n"
            await callback_query.message.delete()
            await callback_query.message.answer(
                message_text,
                reply_markup=account_inline_keyboard(),
                parse_mode='Markdown'
            )
        else:
            await callback_query.answer("У вас нет взносов.", show_alert=True)
    except Exception as e:
        logger.error(f"Ошибка в view_contributions: {e}")


@router.callback_query(F.data == 'view_all_contributions')
async def view_all_contributions(callback_query: CallbackQuery):
    """Просмотр всех взносов."""
    try:
        contributions = await get_all_contributions()
        if contributions:
            total = sum([c['amount'] for c in contributions])
            message_text = f"Все взносы:\nОбщая сумма: *{total}* у.е.\n"
            for c in contributions:
                date = c['date'].split(' ')[0]
                message_text += f"- {c['username']
                                     }: {c['amount']} у.е. от {date}\n"
            await callback_query.message.delete()
            await callback_query.message.answer(
                message_text,
                reply_markup=main_inline_keyboard(),
                parse_mode='Markdown'
            )
        else:
            await callback_query.answer("Взносов пока нет.", show_alert=True)
    except Exception as e:
        logger.error(f"Ошибка в view_all_contributions: {e}")


@router.callback_query(F.data == 'set_role')
async def set_role(callback_query: CallbackQuery):
    """Функция назначения роли пользователю."""
    try:
        await callback_query.answer("Функция назначения роли в разработке.", show_alert=True)
    except Exception as e:
        logger.error(f"Ошибка в set_role: {e}")


def register_handlers(dp: Dispatcher):
    dp.include_router(router)
