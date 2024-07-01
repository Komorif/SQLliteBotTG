import sqlite3 as sq
from aiogram.dispatcher import FSMContext


# Создание таблицы
async def db_start():
    global db, cur
    db = sq.connect('tg.db')
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        name TEXT,
        years INTEGER,
        blogger TEXT,
        hobbies TEXT,
        city TEXT
    )''')
    db.commit()


# задаем "ключи" для каждого столбца
async def add_item(state: FSMContext):
    async with state.proxy() as data:
        cur.execute("INSERT INTO users (user_id, username, name, years, blogger, hobbies, city) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (data['user_id'], data['username'], data['name'], data['years'], data['blogger'], data['hobbies'], data['city']))
        db.commit()


"""
Сортировка по похожести
1) возраст (разница должна быть не более 2 лет)
2) город (не важно написано с caps lock или нет)
"""

async def get_similar_users(user_id, years_range=2):
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    if not user:
        return None

    user_years = user[3]
    user_city = user[6].lower()

    cur.execute("SELECT * FROM users WHERE user_id != ?", (user_id,))
    all_users = cur.fetchall()

    # Подбор пользователей с учетом критерия возраста и города
    similar_users = []
    for u in all_users:
        if abs(u[3] - user_years) <= years_range or u[6].lower() == user_city:
            similar_users.append(u)

    return similar_users


# Для проверки на уникальность user_id
async def user_exists(user_id: int):
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return cur.fetchone()
