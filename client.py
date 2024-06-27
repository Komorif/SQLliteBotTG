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

TOKEN = "xxxx"
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
menu_one = ("https://downloader.disk.yandex.ru/preview/54616eaacb3977dee3660939c498610e98d8bb9fbb7ede6ce98da40a07"
	"110bd6/66782c56/3wfhugOB7CO1Q4XD37T8NweDq5vmVFNBItZJLUJf2ZCT4Y8H854OkMt_JSkqsiJV6zZeADN7D1HA-TxHQ1pM1A%3D%3D?"
	"uid=0&filename=mineShield.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048")


# Менюшка команд бота
async def set_starting_commands(bot: Bot, chat_id: int):
    STARTING_COMMANDS = {
		"ru": [
			BotCommand("start", "Команда start запускает бота, начать сначала"), # /start
			BotCommand("help", "Вывести информацию по боту"), # /help
			BotCommand("id", "Узнать свой id"), # /id
			BotCommand("echo", "Эхо"), # /echo
		],
		"en": [
			BotCommand("start", "Restart bot"), # /start
			BotCommand("help", "Info about bot"), # /help
			BotCommand("id", "Find your id"), # /id
			BotCommand("echo", "Echo"), # /echo
		]
	}
    for language, commands in STARTING_COMMANDS.items():
	    await bot.set_my_commands(
		    commands=commands,
		    scope=BotCommandScopeChat(chat_id),
		    language_code=language
		)


# /start
@dp.message_handler(commands="start")
async def command_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)

    await NewOrder.type.set()

    await set_starting_commands(bot, message.from_user.id)

    await message.answer('Приветствую тебя в боте для нахождения друзей из Майншилд комьюнити! Для начала заполним небольшую анкету. Напиши если готов', reply_markup=back_name)


# /help
@dp.message_handler(commands="help")
async def command_help(message: types.Message):
	await message.answer("Вы можете использовать меня для поиска друзей по интересам")


# /id
@dp.message_handler(commands="id")
async def command_id(message: types.Message):
	await message.answer(f"Ваш id: {message.from_user.id}")


# /echo
@dp.message_handler(commands="echo")
async def command_echo(message: types.Message):
	await message.answer("Если отправить что-то из этого списка"
        					"\n1. Смайлик\n2. Эмоджи\n3. Gif\n4. Видео"
        					"\n4. Фото\n5. Голосовое сообщение\n\nБот отправит вам его в ответ")



# Функция для редактирования инлайн клавиатур
async def edit_message(call: types.CallbackQuery, photo,
                       kb: InlineKeyboardMarkup, caption: str):

	image = InputMediaPhoto(photo)

	await call.message.edit_media(media=image)

	await call.message.edit_caption(caption, parse_mode="HTML")
	await call.message.edit_reply_markup(reply_markup=kb)







    #if call.data == "mainMenu_in_name":
    #    #await edit_message(call, photo=image, caption="Ваше имя", kb=mainMenu_in_name)
#
#
    #    async with state.proxy() as data:
    #    	data["name"] = call.data
#
    #    await call.message.answer(f"Ваше имя: ", reply_markup=mainMenu_in_name)
    #    await NewOrder.next()
#
#
    #    #await NewOrder.name.set()
#
    #elif call.data == "mainMenu_in_years":
    #    await edit_message(call, photo=image, caption="Введите ваш возраст:", kb=mainMenu_in_years)
    #    await NewOrder.years.set()
#
    #elif call.data == "mainMenu_in_blogger":
    #    await edit_message(call, photo=image, caption="Введите вашего любимого блогера:", kb=mainMenu_in_blogger)
    #    await NewOrder.blogger.set()
#
    #elif call.data == "mainMenu_in_hobbies":
    #    await edit_message(call, photo=image, caption="Введите ваше хобби:", kb=mainMenu_in_hobbies)
    #    await NewOrder.hobbies.set()
#
    #elif call.data == "mainMenu_in_city":
    #    await edit_message(call, photo=image, caption="Введите ваш город\nМожно не указывать", kb=mainMenu_in_city)
    #    await NewOrder.city.set()




class NewOrder(StatesGroup):
    type = State()
    name = State()
    years = State()
    blogger = State()
    hobbies = State()
    city = State()





@dp.message_handler(commands="test")
async def add_item(message: types.Message):

    await NewOrder.type.set()
    await message.answer('Выберите что хотите', reply_markup=mainMenu_mineShield)




# тайпим
@dp.callback_query_handler(state=NewOrder.type)
async def typing(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Напишите ваше имя')
    await NewOrder.next()


# имя
@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Введите сколько вам лет')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.years)
async def add_item_years(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['years'] = message.text
    await message.answer('Ваш ютубер')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.blogger)
async def add_item_blogger(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['blogger'] = message.text
    await message.answer('Расскажите о вас')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.hobbies)
async def add_item_hobbies(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hobbies'] = message.text
    await message.answer('Ваш Город')

    await NewOrder.next()


@dp.message_handler(state=NewOrder.city)
async def add_item_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text

    await db.add_item(state)
    await message.answer("Товар успешно создан!")
    await state.finish()














# Register dispather
def register_handlers_client(dp : Dispatcher):
  dp.register_message_handler(command_start, commands=["start"])

if __name__ == "__main__":
	executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
