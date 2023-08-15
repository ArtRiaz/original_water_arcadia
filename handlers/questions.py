from aiogram.types import CallbackQuery
from aiogram import types
from keyboards.inline import ikb_question, inline_questions_back
from aiogram import Dispatcher


async def questions(call: types.CallbackQuery):
    with open('logo.jpg', 'rb') as photo:
        await call.bot.send_photo(chat_id=call.from_user.id, photo=photo)
        await call.message.answer("<b>Очищення води Arcadia</b>\n"
                                  "складається з 8 рівнів!\n"
                                  "\n"
                                  "Завдяки унікальному та сучасному іноземному обладнанню ми робимо воду не тільки "
                                  "смачною, а й безпечною для споживання. Виробництво знаходиться в центрі Одеси, "
                                  "тож переконатися у відповідальному ставленні до процесу очистки можна особисто. ",
                                  reply_markup=ikb_question())


async def question_1(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Робить воду прозорою та захищає від механічних пошкоджень ",
                                  reply_markup=inline_questions_back())


async def question_2(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Позбавлення води від зайвих мінералів та шкідливих солей, та видаляємо важки метали",
                                  reply_markup=inline_questions_back())


async def question_3(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Покращення смаку та запаху води",
                                  reply_markup=inline_questions_back())


async def question_4(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Для цього ми використовуємо систему зворотнього осмосу, це допомогає видалити з води "
        "99% нітратів, фторидів та їншіх забруднень",
        reply_markup=inline_questions_back())


async def question_5(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Озонування води та позбавлення від бактерій",
                                  reply_markup=inline_questions_back())


async def question_6(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("На цьому етапі ми покращуємо смак та запах води",
                                  reply_markup=inline_questions_back())


async def question_7(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Ще одне знезарадження води, яке запобігає появі мікроорганізмів"
                                  "",
                                  reply_markup=inline_questions_back())


async def question_8(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Пункт доочищення та розливу питної води обладнан спеціальним знежаражувальним "
                                  "розчином, щоб зробити ємності якісними та безпечними",
                                  reply_markup=inline_questions_back())


async def inline_cancel(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Відміна", reply_markup=ikb_question())


def question_menu(dp: Dispatcher):
    dp.register_callback_query_handler(questions, text="cleaner")
    dp.register_callback_query_handler(question_1, text='1')
    dp.register_callback_query_handler(question_2, text='2')
    dp.register_callback_query_handler(question_3, text='3')
    dp.register_callback_query_handler(question_4, text='4')
    dp.register_callback_query_handler(question_5, text='5')
    dp.register_callback_query_handler(question_6, text='6')
    dp.register_callback_query_handler(question_7, text='7')
    dp.register_callback_query_handler(question_8, text='8')
    dp.register_callback_query_handler(inline_cancel, text='cancel')
