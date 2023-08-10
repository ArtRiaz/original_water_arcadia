from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from handlers.start import get_kb_menu


async def cmd_back(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Ви повернулись у головне меню, зробить свій вибір:',
                              reply_markup=get_kb_menu())


def register_handler_back(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_back, text="back_general_menu")
