# app/keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Личный кабинет", callback_data="my_account")],
        [InlineKeyboardButton(text="Зарегистрироваться", callback_data="register_user")],
        [InlineKeyboardButton(text="Добавить взнос", callback_data="contribute")],
        [InlineKeyboardButton(text="Назначить роль", callback_data="set_role")],
        [InlineKeyboardButton(text="Просмотреть все взносы", callback_data="view_all_contributions")]
    ])
    return keyboard

def cancel_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_contribution")]
    ])
    return keyboard

def account_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Просмотреть взносы", callback_data="view_contributions")],
        [InlineKeyboardButton(text="Назад в главное меню", callback_data="back_to_main_menu")]
    ])
    return keyboard

def confirm_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_contribution")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_contribution")]
    ])
    return keyboard

async def generate_user_keyboard(get_all_users, page: int = 1):
    USERS_PER_PAGE = 5
    users = await get_all_users()
    start = (page - 1) * USERS_PER_PAGE
    end = start + USERS_PER_PAGE
    users_on_page = users[start:end]
    
    buttons = [
        [InlineKeyboardButton(text=user['username'], callback_data=f"select_user:{user['user_id']}")]
        for user in users_on_page
    ]
    
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Предыдущая", callback_data=f"page:{page-1}"))
    if end < len(users):
        navigation_buttons.append(InlineKeyboardButton(text="➡️ Следующая", callback_data=f"page:{page+1}"))
    if navigation_buttons:
        buttons.append(navigation_buttons)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
