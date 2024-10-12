# app/keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

USERS_PER_PAGE = 5

def main_keyboard():
    buttons = [
        [KeyboardButton(text="Личный кабинет")],
        [KeyboardButton(text="Зарегистрироваться")],
        [KeyboardButton(text="Добавить взнос")],
        [KeyboardButton(text="Назначить роль"), KeyboardButton(text="Просмотреть все взносы")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def cancel_keyboard():
    buttons = [
        [KeyboardButton(text="Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def account_keyboard():
    buttons = [
        [KeyboardButton(text="Просмотреть взносы")],
        [KeyboardButton(text="Назад в главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


async def generate_user_keyboard(get_all_users, page: int = 1):
    users = await get_all_users()  # Используем переданную функцию для получения всех пользователей
    start = (page - 1) * USERS_PER_PAGE
    end = start + USERS_PER_PAGE
    users_on_page = users[start:end]  # Получаем пользователей для текущей страницы
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    for user in users_on_page:
        keyboard.add(InlineKeyboardButton(text=user[1], callback_data=f"select_user:{user[1]}"))
    
    # Добавляем кнопки для навигации между страницами
    if page > 1:
        keyboard.add(InlineKeyboardButton(text="⬅️ Предыдущая", callback_data=f"page:{page-1}"))
    if end < len(users):
        keyboard.add(InlineKeyboardButton(text="➡️ Следующая", callback_data=f"page:{page+1}"))

    return keyboard
