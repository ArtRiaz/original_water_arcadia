import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import config
from service.database import DBCommands

db = DBCommands()
bot = Bot(config.tg_bot.token)
dp = Dispatcher(bot)


class Mailing(StatesGroup):
    Text = State()
    state = State()
    photo = State()


async def send_all(call: types.CallbackQuery):
    await call.message.answer(f'Введіть текст розсилки:')
    await Mailing.Text.set()


async def mailing_text(message: types.Message, state: FSMContext):
    answer = message.text
    markup = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[
        InlineKeyboardButton(text='Додати фото', callback_data='add_photo'),
        InlineKeyboardButton(text='Далі', callback_data='next'),
        InlineKeyboardButton(text='Відмінить', callback_data='quit')
    ]])
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=markup)
    await Mailing.state.set()


async def next_time(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    await state.finish()

    all_user_ids = await db.get_all_user_ids()
    for user in all_user_ids:
        try:
            await bot.send_message(chat_id=user.user_id, text=text)
            await asyncio.sleep(0.33)
        except Exception:
            pass
    await callback.message.answer('Розсилка виконана')


async def add_photo(callback: CallbackQuery):
    await callback.message.answer('Прийшліть фото')
    await Mailing.photo.set()


async def mailing_send(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[
        InlineKeyboardButton(text='Далі', callback_data='next'),
        InlineKeyboardButton(text='Відмінить', callback_data='quit')
    ]])
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)


async def start_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()

    all_user_ids = await db.get_all_user_ids()
    for user in all_user_ids:
        try:
            await bot.send_photo(chat_id=user.user_id, photo=photo, caption=text)
            await asyncio.sleep(0.33)
        except Exception:
            pass
    await callback.message.answer('Розсилка виконана')


async def no_photo(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[
        InlineKeyboardButton(text='Відмінить', callback_data='quit')
    ]])
    await message.answer('Прийшліть фото', reply_markup=markup)


async def quit_send(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer('Розсилка відмінена')


def register_handler_mailing(dp: Dispatcher):
    dp.register_callback_query_handler(send_all, text='send', user_id=config.tg_bot.admin_ids)
    dp.register_message_handler(mailing_text, state=Mailing.Text, user_id=config.tg_bot.admin_ids)
    dp.register_callback_query_handler(add_photo, text='add_photo', state=Mailing.state,
                                       user_id=config.tg_bot.admin_ids)
    dp.register_message_handler(mailing_send, state=Mailing.photo, content_types=types.ContentType.PHOTO,
                                user_id=config.tg_bot.admin_ids)
    dp.register_message_handler(no_photo, state=Mailing.photo, user_id=config.tg_bot.admin_ids)
    dp.register_callback_query_handler(quit_send, text='quit',
                                       state=[Mailing.Text, Mailing.photo, Mailing.state],
                                       user_id=config.tg_bot.admin_ids)
    dp.register_callback_query_handler(start_next, text='next', state=Mailing.photo, user_id=config.tg_bot.admin_ids)
    dp.register_callback_query_handler(next_time, text='next', state=Mailing.state, user_id=config.tg_bot.admin_ids)
