from aiogram import types, Dispatcher
from keyboards.reply import get_back


async def cmd_calendar(call: types.CallbackQuery):
    with open('logo.jpg', 'rb') as photo:
        await call.bot.send_photo(chat_id=call.from_user.id, photo=photo, caption='<b>Ми працюєм кожен день з 9:00 по '
                                                                                  '19:00\n'
                                                                                  'Розвозимо воду: з 6:00 до 22:00</b>',
                                  reply_markup=get_back())


def handler_calendar(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_calendar, text="work")
