from aiogram.utils import executor

import logging
from aiogram import Bot, Dispatcher, types, executor

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, callback_query

# Объекты для команд бота
from aiogram.types import BotCommand, BotCommandScopeChat

from aiogram.types import InputMediaPhoto

from aiogram.utils.markdown import link

from aiogram import types

from keyboards import *

import database as db

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = "xxxxx"
logging.basicConfig(level=logging.INFO)


# прокси
proxy_url = "xxxxx"


bot = Bot(token=TOKEN, proxy=proxy_url)


dp = Dispatcher(bot, storage = MemoryStorage())

# Функция (запуск бота)
async def on_startup(dp):
	await db.db_start()
	await bot.send_message(xxxxx, "Я запустился")

# Функция (выключение бота)
async def on_shutdown(dp):
	await bot.send_message(xxxxx, "Я завершил работу")


# Картинки для менюшек
menu_one = ("https://downloader.disk.yandex.ru/preview/9775edefc1cd8d1b6b97c8df41de6a2c75ded5ac83eb53c75c95517a9"
"780bbc4/667de652/PkWqoprUG_PqkzoRValuLuXRSIQkQ4YbnI3IfLP-YQSxNfPYUaxwx9Np30W0zI1kSwjgne4qJwjGYr5VY3wPtw%3D%3D?ui"
"d=0&filename=photo_2024-06-23_16-12-56.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048")


# Менюшка команд бота
async def set_starting_commands(bot: Bot, chat_id: int):
    STARTING_COMMANDS = {
		"ru": [
			BotCommand("start", "Команда start запускает бота, начать сначала"), # /start
			BotCommand("help", "Вывести информацию по боту"), # /help
			BotCommand("id", "Узнать свой id"), # /id
		],
		"en": [
			BotCommand("start", "Restart bot"), # /start
			BotCommand("help", "Info about bot"), # /help
			BotCommand("id", "Find your id"), # /id
		]
	}
    for language, commands in STARTING_COMMANDS.items():
	    await bot.set_my_commands(
		    commands=commands,
		    scope=BotCommandScopeChat(chat_id),
		    language_code=language
		)


# Флаг


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await NewOrder.type.set()
    image=menu_one
    await message.answer_photo(photo=image, caption='Приветствую тебя в боте для нахождения друзей из Майншилд комьюнити!\nДля начала заполним небольшую анкету.', reply_markup=mainMenu_mineShield)



# /help
@dp.message_handler(commands="help")
async def command_help(message: types.Message):
	await message.answer("Вы можете использовать меня для поиска друзей по интересам")


# /id
@dp.message_handler(commands="id")
async def command_id(message: types.Message):
	await message.answer(f"Ваш id: {message.from_user.id}")



class NewOrder(StatesGroup):
    type = State()
    name = State()
    years = State()
    blogger = State()
    hobbies = State()
    city = State()



# Имя
@dp.callback_query_handler(state=NewOrder.type)
async def typing(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Напишите ваше имя')
    await NewOrder.next()


# Возраст
@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Введите ваш возраст')
    await NewOrder.next()


# Ютуб
@dp.message_handler(state=NewOrder.years)
async def add_item_years(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['years'] = message.text
    await message.answer('Любимый блогер (из мш и мша)')
    await NewOrder.next()


# О себе
@dp.message_handler(state=NewOrder.blogger)
async def add_item_blogger(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['blogger'] = message.text
    await message.answer('Расскажите о себе')
    await NewOrder.next()


# Город
@dp.message_handler(state=NewOrder.hobbies)
async def add_item_hobbies(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hobbies'] = message.text
    await message.answer('Ваш Город(можно не указывать)')

    await NewOrder.next()


# Конец
@dp.message_handler(state=NewOrder.city)
async def add_item_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text

    await db.add_item(state)
    await message.answer("вы успешно зарегистрировались!")
    await state.finish()



# Register dispather
def register_handlers_client(dp : Dispatcher):
  dp.register_message_handler(command_start, commands=["start"])

if __name__ == "__main__":
	executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
