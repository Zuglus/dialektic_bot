# queries.py
from .models import Database

# Добавление нового пользователя в базу данных
async def add_user(username, chat_id):
    db = Database()
    await db.execute('INSERT INTO users (username, chat_id) VALUES (?, ?)', (username, chat_id))

# Получение информации о пользователе по имени пользователя
async def get_user(username):
    db = Database()
    return await db.fetchone('SELECT id, role FROM users WHERE username = ?', (username,))

# Добавление взноса в базу данных
async def add_contribution(user_id, amount, date):
    db = Database()
    await db.execute('INSERT INTO contributions (user_id, amount, date) VALUES (?, ?, ?)', (user_id, amount, date))

# Получение всех взносов пользователя
async def get_contributions(user_id):
    db = Database()
    return await db.fetchall('SELECT amount, date FROM contributions WHERE user_id = ?', (user_id,))

# Получение всех взносов всех пользователей
async def get_all_contributions():
    db = Database()
    return await db.fetchall('''
        SELECT users.username, contributions.amount, contributions.date
        FROM contributions
        JOIN users ON contributions.user_id = users.id
    ''')
