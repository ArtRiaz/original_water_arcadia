from keyboards.inline import ikb_contact
from aiogram import types, Dispatcher
from tg_bot.keyboards.reply import get_back


async def cmd_contact(call: types.CallbackQuery):
    await call.message.answer('Виберіть мережу або номер телефону:', reply_markup=ikb_contact())
    await call.message.edit_reply_markup()


async def send_geo(callback: types.CallbackQuery):
    await callback.message.bot.send_location(chat_id=callback.from_user.id,
                                             latitude=46.4698845,
                                             longitude=30.7390622,
                                             reply_markup=get_back()
                                             )


async def send_phone(callback: types.CallbackQuery):
    await callback.message.bot.send_contact(chat_id=callback.from_user.id,
                                            phone_number='+38068-555-77-12',
                                            first_name='Замовлення води',
                                            reply_markup=get_back())


def register_handler_contact(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_contact, text="contact_menu")
    dp.register_callback_query_handler(send_geo, text='Геолокация')
    dp.register_callback_query_handler(send_phone, text='Вызов')
