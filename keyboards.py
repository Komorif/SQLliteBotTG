from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, callback_query


# Клавиатуры
mainMenu_mineShield = InlineKeyboardMarkup(row_width=2)
mainMenu_in_registration = InlineKeyboardButton(text="Заполнить анкету", callback_data="mainMenu_in_registration")

mainMenu_mineShield.add(mainMenu_in_registration)

like_button = InlineKeyboardMarkup(row_width=2)
like = InlineKeyboardButton(text="Нравится💘", callback_data="like")

like_button.add(like)
