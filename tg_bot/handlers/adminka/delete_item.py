from aiogram import types, Dispatcher
from tg_bot.service.database import DBCommands
from aiogram.utils.callback_data import CallbackData
import asyncio
from tg_bot.keyboards.inline import back_menu_admin_panel

buy_item = CallbackData("buy", "item_id")
db = DBCommands()


async def delete_items(call: types.CallbackQuery):
    all_items = await db.show_items()
    text = "<b>Товар:</b> {name}\n" \
           "<b>Опис:</b> {description}\n" \
           "<b>Ціна:</b> \t{price:,} UAH\n"
    for item in all_items:
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton("❌ Видалити", callback_data=f"del {item.name}")
        ]])
        await call.bot.send_photo(chat_id=call.from_user.id,
                                  photo=item.photo,
                                  caption=text.format(id=item.id,
                                                      name=item.name,
                                                      description=item.description,
                                                      price=item.price / 100),
                                  reply_markup=markup
                                  )
        await asyncio.sleep(0.33)
    await call.message.answer('Хочете вийти, натисніть <b>"Hазад у головне меню</b>"',
                              reply_markup=back_menu_admin_panel())


async def del_callback_run(callback_query: types.CallbackQuery):
    await db.del_item(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f"видалено")


def register_delete_items(dp: Dispatcher):
    dp.register_callback_query_handler(delete_items, text="delete_item")
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
