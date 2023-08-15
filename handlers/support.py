from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards.inline_support import support_keyboard, support_callback
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_back



async def ask_support(call: types.CallbackQuery):
    text = 'Якщо ви хочите написати у техпідтримку, нажміть кнопку нище'
    keyboard = await support_keyboard(messages='one')
    await call.message.answer(text, reply_markup=keyboard)


async def send_to_support(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await callback.answer()
    user_id = int(callback_data.get('user_id'))

    await callback.message.answer('Пришліть ваше повідомлення: ')
    await state.set_state('wait_for_support_message')
    await state.update_data(second_id=user_id)


async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get('second_id')

    await message.bot.send_message(second_id,
                                   f"Вам прийшло пісьмо! Ви можете відправити натиснув на кнопку нище")
    keyboard = await support_keyboard(messages='one', user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)

    await message.answer('Ви відправили повідомлення', reply_markup=get_back())
    await state.reset_state()


def get_support(dp: Dispatcher):
    dp.register_callback_query_handler(ask_support, text="online")
    dp.register_callback_query_handler(send_to_support, support_callback.filter(messages='one'))
    dp.register_message_handler(get_support_message, state="wait_for_support_message",
                                content_types=types.ContentTypes.ANY)
