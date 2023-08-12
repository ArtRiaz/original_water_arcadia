from asyncio import sleep

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.keyboards.inline import menu_admin_panel, back_menu_admin_panel
from tg_bot.config import load_config
from aiogram.dispatcher.filters import Text
from tg_bot.misc.states import NewItem
from tg_bot.service.database import Item, User

config = load_config()


# Админ панель
async def admin_panel(message: types.Message):
    await message.answer_sticker(sticker="CAACAgEAAxkBAAEJ78Bkz6Cp-U71pthpElEDBxjIfT8VdAACMQIAAoKgIEQHCzBVrLHGhy8E")
    await sleep(3)
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEJ76Rkz5pVqYHtFcLn9EwC2gpAqT-R8wACxgEAAhZCawpKI9T0ydt5Ry8E")
    await message.answer("Привіт Адмін!!!!", reply_markup=menu_admin_panel())


# Назад в админ панель

async def back_admin(call: types.CallbackQuery):
    await call.message.answer("Ви повернулись у меню адміна", reply_markup=menu_admin_panel())


"""Создание товара"""


async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Ви відмінили створення товара")
    await state.reset_state()


async def add_item(call: types.CallbackQuery):
    await call.message.answer("Введіть назву товара або натисніть /cancel")
    await NewItem.Name.set()


async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    item = Item()
    item.name = name

    await message.answer("Назва: {name}"
                         "\nНадішліть мені фотографію товара (не документ) або  натисніть /cancel".format(
        name=item.name))

    await NewItem.Photo.set()
    check = await state.update_data(item=item)
    print(check)


async def add_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    item: Item = data.get("item")
    item.photo = photo

    print(photo)
    print(item.photo)

    await message.answer_photo(
        photo=photo,
        caption=("Назва: {name}"
                 "\nВведить опис або натисніть /cancel".format(name=item.name)))

    await NewItem.Description.set()
    await state.update_data(item=item)


async def enter_desc(message: types.Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    item: Item = data.get("item")
    item.description = description
    print(description)
    await message.answer("Назва: {name}\n"
                         "Опис: {description}\n"
                         "Введить ціну товара у копійках або натисніть /cancel".format(name=item.name,
                                                                                       description=description))

    await NewItem.Price.set()
    check = await state.update_data(item=item)
    print(check)


async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")
    try:
        price = int(message.text)
    except ValueError:
        await message.answer("Невірне значення, введіть число")
        return

    item.price = price
    print(price)
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Так", callback_data="confirm")],
            [InlineKeyboardButton(text="Введить знову", callback_data="change")],
        ]
    )
    await message.answer("Ціна: {price:,}\n"
                         "Підтведжуйте? Натисніть /cancel щоб відмінити".format(price=price / 100),
                         reply_markup=markup)
    await state.update_data(item=item)
    await NewItem.Confirm.set()


async def change_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Введить знову ціну товара у копійках")
    await NewItem.Price.set()


async def confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get("item")
    await item.create()
    await call.message.answer("Товар вдало створен.", reply_markup=back_menu_admin_panel())
    await state.reset_state()


def register_handler_create_items(dp: Dispatcher):
    dp.register_message_handler(cancel, user_id=config.tg_bot.admin_ids, commands=["cancel"], state=NewItem)
    dp.register_message_handler(admin_panel, Text(equals="Admin"), user_id=config.tg_bot.admin_ids)
    dp.register_callback_query_handler(back_admin, text="back_admin_panel")
    dp.register_callback_query_handler(add_item, user_id=config.tg_bot.admin_ids, text="add_item")
    dp.register_message_handler(enter_name, user_id=config.tg_bot.admin_ids, state=NewItem.Name)
    dp.register_message_handler(add_photo, user_id=config.tg_bot.admin_ids, state=NewItem.Photo,
                                content_types=types.ContentType.PHOTO)
    dp.register_message_handler(enter_desc, user_id=config.tg_bot.admin_ids, state=NewItem.Description)
    dp.register_message_handler(enter_price, user_id=config.tg_bot.admin_ids, state=NewItem.Price)
    dp.register_callback_query_handler(change_price, user_id=config.tg_bot.admin_ids, text_contains="change",
                                       state=NewItem.Confirm)
    dp.register_callback_query_handler(confirm, user_id=config.tg_bot.admin_ids, text_contains="confirm",
                                       state=NewItem.Confirm)
