from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, callback_query


# Клавиатура номер 1 (Главная)
mainMenu_mineShield = InlineKeyboardMarkup(row_width=2)
mainMenu_in_name = InlineKeyboardButton(text="Имя пользователя🧒", callback_data="mainMenu_in_name")
mainMenu_in_years = InlineKeyboardButton(text="Возраст❓", callback_data="mainMenu_in_years")
mainMenu_in_brogger = InlineKeyboardButton(text="Любимый блогер✏", callback_data="mainMenu_in_brogger")
mainMenu_in_hobbies = InlineKeyboardButton(text="Хобби💰", callback_data="mainMenu_in_hobbies")
mainMenu_in_city = InlineKeyboardButton(text="Город", callback_data="mainMenu_in_city")

mainMenu_mineShield.add(mainMenu_in_name, mainMenu_in_years).add(mainMenu_in_brogger, mainMenu_in_hobbies)
mainMenu_mineShield.add(mainMenu_in_city)


# Клавиатура номер 2 (Имя пользователя)
mainMenu_in_name = InlineKeyboardMarkup(row_width=2)
back_name = InlineKeyboardButton(text="Назад", callback_data="back_name")

mainMenu_in_name.add(back_name)


# Клавиатура номер 3 (Возраст)
mainMenu_in_years = InlineKeyboardMarkup(row_width=2)
back_years = InlineKeyboardButton(text="Назад", callback_data="back_years")

mainMenu_in_years.add(back_years)


# Клавиатура номер 4 (Любимый блогер)
mainMenu_in_brogger = InlineKeyboardMarkup(row_width=2)
back_blogger = InlineKeyboardButton(text="Назад", callback_data="back_blogger")

mainMenu_in_brogger.add(back_blogger)


# Клавиатура номер 5 (Хобби)
mainMenu_in_hobbies = InlineKeyboardMarkup(row_width=2)
back_hobbies = InlineKeyboardButton(text="Назад", callback_data="back_hobbies")

mainMenu_in_hobbies.add(back_hobbies)


# Клавиатура номер 6 (Город)
mainMenu_in_city = InlineKeyboardMarkup(row_width=2)

mainMenu_in_delete = InlineKeyboardButton(text="Не хочу рассказывать", callback_data="back_city")
back_city = InlineKeyboardButton(text="Назад", callback_data="back_city")

mainMenu_in_city.add(back_city)