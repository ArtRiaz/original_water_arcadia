import asyncio

from aiogram import types, Dispatcher
from tg_bot.keyboards.reply import kb_menu, get_kb_menu, get_back, get_sertificate
from aiogram.dispatcher.filters import Text


async def cmd_menu(call: types.CallbackQuery):
    with open('logo.jpg', 'rb') as photo:
        await call.message.delete()
        await call.message.bot.send_photo(chat_id=call.from_user.id,
                                          photo=photo,
                                          caption=f'<b>Вода «Arcadia» завдяки природному походження нашої води, вона не '
                                                  f'просто смачна'
                                                  f'сама по собі, а й дарує незабутній смак усім вашим стравам та '
                                                  f'напоям.</b>',
                                          reply_markup=get_sertificate())


async def sertificate(call: types.CallbackQuery):
    with open("water_doc1.jpg", "rb") as photo1:
        await call.message.bot.send_photo(chat_id=call.from_user.id,
                                          photo=photo1,
                                          caption="Висновок державної санітарно-епідеміологічної експертизи")
    await asyncio.sleep(1)
    with open("water_doc2.jpg", "rb") as photo2:
        await call.message.bot.send_photo(chat_id=call.from_user.id,
                                          photo=photo2,
                                          caption="Протокол № 428", reply_markup=get_back())


def register_handlers_about(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_menu, text="our_company")
    dp.register_callback_query_handler(sertificate, text="sertif_menu")