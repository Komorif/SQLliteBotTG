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
			BotCommand("find_similar", "Найти единомышлиников"), # /find_similar
		],
		"en": [
			BotCommand("start", "Restart bot"), # /start
			BotCommand("help", "Info about bot"), # /help
			BotCommand("id", "Find your id"), # /id
			BotCommand("find_similar", "Find like-minded people"), # /find_similar
		]
	}
    for language, commands in STARTING_COMMANDS.items():
	    await bot.set_my_commands(
		    commands=commands,
		    scope=BotCommandScopeChat(chat_id),
		    language_code=language
		)


# /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):

    user_id = message.from_user.id

    # Если id пользователя внесен в БД
    if await db.user_exists(user_id):
        await message.answer("Вы уже зарегистрировались!")

    # Если id пользователя новый
    else:
        await NewOrder.type.set()

        image = menu_one
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
        data['user_id'] = call.from_user.id
        data['username'] = call.from_user.username

    await call.message.answer('Введите ваше имя')
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
    await message.answer('Любимый блогер (из мш и мша (можно несколько))')
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
    await message.answer('Ваш Город(можно не указывать - пропишите нет)')

    await NewOrder.next()


# Конец
@dp.message_handler(state=NewOrder.city)
async def add_item_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text

    await db.add_item(state)
    await message.answer("Вы успешно зарегистрировались!")
    await state.finish()




from aiogram.dispatcher.filters import Text

# /find_similar
@dp.message_handler(commands='find_similar')
async def find_similar(message: types.Message):
    user_id = message.from_user.id
    similar_users = await db.get_similar_users(user_id)

    if not similar_users:
        await message.answer("Для вас не найдено пользователей с похожими параметрами(")
        return

    for user in similar_users:

        image = menu_one

        await message.answer_photo(photo=image,
            caption=f"Пользователь с которым возможно вы найдете общий язык\n\n"
            f"Ник: @{user[1]}\n"
            f"Имя: {user[2]}\n"
            f"Возраст: {user[3]}\n"
            f"Любимый блогер: {user[4]}\n"
            f"О себе: {user[5]}\n"
            f"Город: {user[6]}", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Нравится💘", callback_data=f"like_{user[1]}"))
        )





@dp.callback_query_handler(lambda c: c.data and c.data.startswith('like_'))
async def process_callback_like(callback_query: types.CallbackQuery):
    username = callback_query.data.split('_')[1]  # Получаем имя пользователя из callback_data
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=f"Для начала общения напишите @{username}\nУдачного общения!"
    )
    await bot.answer_callback_query(callback_query.id)






# Register dispather
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
