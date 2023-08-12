from aiogram import types, Dispatcher
from tg_bot.keyboards.reply import kb_menu, get_kb_menu, get_back
from aiogram.dispatcher.filters import Text
from tg_bot.service.database import DBCommands, create_db, Item
from tg_bot.service import database
from tg_bot.config import load_config, PAYMENT_TOKEN
from aiogram import Bot
import asyncio
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import FSMContext
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery, ShippingQuery, \
    ShippingOption, ReplyKeyboardMarkup, KeyboardButton
from tg_bot.misc import states
from aiogram.types.message import ContentType
from tg_bot.keyboards.inline import menu_cart, pay_cash_or_card
from tg_bot.models.shipping import POST_REGULAR_SHIPPING
import pytz

bot = Bot
db = DBCommands()
config = load_config()
buy_item = CallbackData("buy", "item_id")


async def cmd_start(call: types.CallbackQuery):
    with open('arc.jpg', 'rb') as photo:
        await create_db()

        chat_id = call.from_user.id
        await db.add_new_user()
        await call.bot.send_photo(chat_id=chat_id,
                                  photo=photo,
                                  caption=f'<b>Вітаю Вас {call.from_user.full_name}!\n'
                                          "Вода «Arcadia», завдяки природному походженню нашої води, вона не "
                                          "просто смачна"
                                          "сама по собі, а й дарує"
                                          "незабутній смак усім вашим стравам та напоям.</b>\n "
                                          "\n"
                                          "Компанія заснована у квітні цього року. Завдяки ретельній та глибокій "
                                          "очистці"
                                          "вода Arcadia смакує так, наче пʼєте її безпосередньо з джерела. "
                                          "Готуйте смачні напої та розкрийте смак ваших страв, підтримуйте водний "
                                          "баланс"
                                          "та втамовуйте спрагу. "
                                          "Ми набираємо свіжу кришталево чисту воду у пляшки перед кожною "
                                          "відправкою.Доставляємо по місту! "
                                  , reply_markup=kb_menu())


async def cmd_menu(call: types.CallbackQuery):
    await call.message.answer('Управління меню', reply_markup=get_kb_menu())


async def show_items(call: types.CallbackQuery):
    all_items = await db.show_items()
    text = "<b>Товар:</b> {name}\n" \
           "<b>Опис:</b> {description}\n" \
           "<b>Ціна:</b> \t{price:,} UAH\n"
    for item in all_items:
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton("☑️ Замовити", callback_data=buy_item.new(item_id=item.id))
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
    await call.message.answer('Хочете вийти, натисніть <b>"Hазад у головне меню"</b>',
                              reply_markup=get_back())


async def empty_cart(call: types.CallbackQuery):
    user_id = call.from_user.id
    sticker = "CAACAgEAAxkBAAEJ7N9kzWIUHWUvKjjuDieMJBrJoqWegQACDwIAAlCNKEcb6ebEddn2-i8E"
    await db.empty_cart(user_id)
    await call.bot.send_sticker(chat_id=call.from_user.id, sticker=sticker)
    await call.message.answer("Ваш кошик порожній...", )


async def buying(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = int(callback_data.get("item_id"))
    await call.message.edit_reply_markup()
    item = await database.Item.get(item_id)
    if not item:
        await call.message.answer("Такого товара немає")
        return
    text = "Бажаєте замовити <b>{name}</b>\n" \
           "за ціною <b>{price:,}</b> UAH\n" \
           "Введить кількість товара: ".format(name=item.name,
                                               price=item.price / 100)
    await call.message.answer(text)
    await states.Purchase.EnterQuantity.set()
    await state.update_data(
        item=item,
        purchase=database.Purchase(
            item_id=item_id,
            purchase_time=datetime.datetime.now(),
            buyer=call.from_user.id,
            name=item.name
        )
    )


async def enter_quantity(message: types.Message, state: FSMContext):
    quantity = int(message.text)
    async with state.proxy() as data:
        data["purchase"].quantity = quantity
        item = data.get("item")
        amount = item.price * quantity
        data["purchase"].amount = amount

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="☑️ Додати у кошик",
                callback_data="agree")],
        [
            InlineKeyboardButton(text="🔁 Ввести кількість знову",
                                 callback_data="change")
        ], [
            InlineKeyboardButton(
                text="❌ Відмінити замовлення",
                callback_data="cancel")
        ]])

    await states.Purchase.Approval.set()

    await message.answer(
        "Добре, бажаєте купити {quantity} шт. <b>{name}</b> за ціною <b>{price:,} UAH</b>\n"
        "Вийде <b>{amount:,} UAH</b>. Ви підтверджуйте ?".format(
            quantity=quantity,
            name=item.name,
            amount=amount / 100,
            price=item.price / 100
        ),
        reply_markup=markup)
    await states.Purchase.Approval.set()


# То, что не является числом - не попало в предыдущий хендлер и попадает в этот
async def not_quantity(message: types.Message):
    await message.answer("Невірне значення, введіть число")


# Если человек нажал на кнопку Отменить во время покупки - убираем все
async def approval(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()  # Убираем кнопки
    await call.message.answer("Ви відмінили замовлення", reply_markup=get_back())
    await state.reset_state()


# Если человек нажал "ввести заново"
async def again(call: types.CallbackQuery):
    await call.message.edit_reply_markup()  # Убираем кнопки
    await call.message.answer("Введить кількість товара знову.")
    await states.Purchase.EnterQuantity.set()


# Если человек нажал "согласен"
async def enter_agree(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()  # Убираем кнопки

    data = await state.get_data()
    purchase = data.get("purchase")
    item = data.get("item")
    # Теперь можно внести данные о покупке в базу данных через .create()
    await purchase.create()
    await call.message.answer('Добре! Якщо бажаєте замовити ще товар, натисніть кнопку нище,\n'
                              ' або перейдить у <b>"Моя корзина"</b> для сплати товару ',
                              reply_markup=InlineKeyboardMarkup(
                                  inline_keyboard=[[
                                      InlineKeyboardButton("🏁 Оформить ще замовлення", callback_data="do_order"),
                                      InlineKeyboardButton("🛒 Мій кошик", callback_data="my_cart")
                                  ]]
                              ))
    await state.reset_state()


# Выбор способа оплаты
async def check_pay(call: types.CallbackQuery):
    await call.message.answer("Виберіть засіб оплати", reply_markup=pay_cash_or_card())


# Моя корзина
async def my_cart(call: types.CallbackQuery):
    user_id = call.from_user.id
    summa = 0
    all_cart = await db.show_cart(user_id)
    all_items_text = "🛒 Кошик:\n" \
                     "\n"
    for num, cart in enumerate(all_cart, start=1):
        amount = cart.amount / 100
        summa += amount
        all_items_text += f"{num} {cart.name} = {amount} UAH\n"
    await call.message.answer(all_items_text)
    await call.message.answer(f"💵 Всього: {summa}UAH", reply_markup=menu_cart())


# Оплата наличными, регистрация
async def pay_cash(call: types.CallbackQuery):
    await call.message.answer("Бажаєте разрахуватись <b>готівкою</b> при отриманні товару, введить свои данні та адресу"
                              "доставки")
    await states.OrderItems.Name.set()
    await call.message.answer("Введить своє ім'я:")


# Регестрируем имя
async def pay_cash_name(message: types.Message, state: FSMContext):
    name = message.text
    register = states.OrderItems()
    register.name = name
    await states.OrderItems.next()
    await state.update_data(register=register)
    await message.reply("Введіть свій контактний номер телефону: ")


# регестрируем номер тел.
async def pay_cash_phone(message: types.Message, state: FSMContext):
    if all(c.isdigit() or c == "+" for c in message.text):  # проверка на цифры и символ +
        phone = message.text
        data = await state.get_data()
        register = data.get("register")
        register.phone = phone
        await state.update_data(register=register)
        await states.OrderItems.next()
        await message.answer("Введиіть свою адресу доставки:")
    else:
        await message.answer("Введить вірний номер")


# Регестрируем адрес
async def pay_cash_adress(message: types.Message, state: FSMContext):
    adress = message.text
    data = await state.get_data()
    register = data.get("register")
    register.adress = adress
    await state.update_data(register=register)

    text = f"Вам прийшов заказ:\n" \
           f"Дата: {datetime.datetime.now(tz=pytz.timezone('Europe/Kiev'))}\n" \
           f"Ваше ім'я: {register.name}\n" \
           f"Ваш номер телефону: {register.phone}\n" \
           f"Ваша адреса: {register.adress}\n" \
           f"<b>Оплата готівкою</b>"

    await message.bot.send_sticker(chat_id=message.from_user.id,
                                   sticker="CAACAgIAAxkBAAEJ7nNkzq1jPENuM1E0IY9osPMRyBpwWwACogEAAhZCawqhd3djmk6DIS8E")
    await message.answer("Ваше замовлення було відправлено.\n"
                         "Наш менеджер зв'яжется з Вами найблищим часом")

    user_id = message.from_user.id
    summa = 0
    all_cart = await db.show_cart(user_id)
    all_items_text = "Товари замовлення:\n" \
                     "\n"
    for num, cart in enumerate(all_cart, start=1):
        amount = cart.amount / 100
        summa += amount
        all_items_text += f"{num} {cart.name} = {amount} UAH\n"

    for admin in config.tg_bot.admin_ids:
        await message.bot.send_message(chat_id=admin, text=text)
        await message.bot.send_message(chat_id=admin, text=all_items_text)
        await message.bot.send_message(chat_id=admin, text=f"💵 Всього: {summa}UAH")

        # Очистить корзину после оплаты
        await db.empty_cart(user_id)
        # Сбросить состояние
        await state.reset_state()

    return


# Оплата курьеру карточкой, регистрация
async def pay_card_cur(call: types.CallbackQuery):
    await call.message.answer("Бажаєте разрахуватись <b>карткою</b> при отриманні товару, введить свои данні та адресу "
                              "доставки")
    await states.OrderCard.Name_card.set()
    await call.message.answer("Введить своє ім'я:")


# Регистрация имя
async def pay_card_name(message: types.Message, state: FSMContext):
    name = message.text
    register = states.OrderCard()
    register.name = name
    await states.OrderCard.next()
    await state.update_data(register=register)
    await message.reply("Введіть свій контактний номер телефону: ")


# Регистрация телефона
async def pay_card_phone(message: types.Message, state: FSMContext):
    if all(c.isdigit() or c == "+" for c in message.text):  # проверка на цифры и символ +
        phone = message.text
        data = await state.get_data()
        register = data.get("register")
        register.phone = phone
        await state.update_data(register=register)
        await states.OrderCard.next()
        await message.answer("Введиіть свою адресу доставки:")
    else:
        await message.answer("Введить вірний номер")


# Регистрация адреса
async def pay_card_adress(message: types.Message, state: FSMContext):
    adress = message.text
    data = await state.get_data()
    register = data.get("register")
    register.adress = adress
    await state.update_data(register=register)

    text = f"Вам прийшов заказ:\n" \
           f"Дата: {datetime.datetime.now(tz=pytz.timezone('Europe/Kiev'))}\n" \
           f"Ваше ім'я: {register.name}\n" \
           f"Ваш номер телефону: {register.phone}\n" \
           f"Ваша адреса: {register.adress}\n" \
           f"<b>Оплата карткою, будь ласка не забудьте взяти термінал</b>"

    await message.bot.send_sticker(chat_id=message.from_user.id,
                                   sticker="CAACAgIAAxkBAAEJ7nNkzq1jPENuM1E0IY9osPMRyBpwWwACogEAAhZCawqhd3djmk6DIS8E")
    await message.answer("Ваше замовлення було відправлено.\n"
                         "Наш менеджер зв'яжется з Вами найблищим часом")

    user_id = message.from_user.id
    summa = 0
    all_cart = await db.show_cart(user_id)
    all_items_text = "Товари замовлення:\n" \
                     "\n"
    for num, cart in enumerate(all_cart, start=1):
        amount = cart.amount / 100
        summa += amount
        all_items_text += f"{num} {cart.name} = {amount} UAH\n"

    for admin in config.tg_bot.admin_ids:
        await message.bot.send_message(chat_id=admin, text=text)
        await message.bot.send_message(chat_id=admin, text=all_items_text)
        await message.bot.send_message(chat_id=admin, text=f"💵 Всього: {summa}UAH")

        # Очистить корзину после оплаты
        await db.empty_cart(user_id)
        # Сбросить состояние
        await state.reset_state()


# Оплата через бот
async def pay(call: types.CallbackQuery):
    user_id = call.from_user.id
    summa = 0
    all_cart = await db.show_cart(user_id)

    for cart in all_cart:
        amount = cart.amount
        summa += amount
    prices = [LabeledPrice(label="Arcadia", amount=summa)]

    await call.bot.send_invoice(chat_id=call.from_user.id,
                                title="Arcadia",
                                description="Доставка води",
                                payload="some",
                                start_parameter="example",
                                currency="UAH",
                                prices=prices,
                                provider_token=PAYMENT_TOKEN,
                                need_name=True,
                                need_phone_number=True,
                                need_email=False,
                                need_shipping_address=True,
                                is_flexible=True
                                )


# Доставка
async def choose_shipping_city(query: ShippingQuery):
    if query.shipping_address.city == "Одесса" or "Одеса":
        await query.bot.answer_shipping_query(
            shipping_query_id=query.id,
            shipping_options=[POST_REGULAR_SHIPPING],
            ok=True)
    elif not query.shipping_address.city == "Одесса" or "Одеса":
        await query.bot.answer_shipping_query(shipping_query_id=query.id,
                                              ok=False,
                                              error_message="У це місто не доставляємо, працюєм тількі по Одесі")


async def checkout(query: PreCheckoutQuery):
    user_id = query.from_user.id
    await query.bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
    all_cart = await db.show_cart(user_id)
    all_items_text = "Ви отримали замовлення:\n" \
                     "\n"
    for num, cart in enumerate(all_cart, start=1):
        amount = cart.amount / 100
        all_items_text += f"{num} {cart.name} = {amount} UAH\n"

    await query.bot.send_sticker(chat_id=query.from_user.id,
                                 sticker="CAACAgIAAxkBAAEJ7nNkzq1jPENuM1E0IY9osPMRyBpwWwACogEAAhZCawqhd3djmk6DIS8E")
    await query.bot.send_message(chat_id=query.from_user.id, text=f"Ваше замовлення було відправлено.\n"
                                                                  "Наш менеджер зв'яжется з Вами найблищим часом")

    for admin in config.tg_bot.admin_ids:
        await query.bot.send_message(chat_id=admin,
                                     text=f'Дата: {datetime.datetime.now(tz=pytz.timezone("Europe/Kiev"))}\n'
                                          f"Товар: {all_items_text}\n"
                                          f"Номер телефону: {query.order_info.phone_number}\n"
                                          f"Адреса: {query.order_info.shipping_address.city}, "
                                          f"{query.order_info.shipping_address.street_line1}\n"
                                          f"Сума: {query.total_amount / 100} UAH")

    # Очистить корзину после оплаты
    await db.empty_cart(user_id)


def register_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_callback_query_handler(cmd_menu, text="general_menu")
    dp.register_callback_query_handler(show_items, text="do_order")
    dp.register_callback_query_handler(empty_cart, text="reset_cart")
    dp.register_callback_query_handler(buying, buy_item.filter())
    dp.register_message_handler(enter_quantity, regexp=r"^(\d+)$", state=states.Purchase.EnterQuantity)
    dp.register_message_handler(not_quantity, state=states.Purchase.EnterQuantity)
    dp.register_callback_query_handler(approval, text_contains="cancel", state=states.Purchase)
    dp.register_callback_query_handler(again, text_contains="change", state=states.Purchase.Approval)
    dp.register_callback_query_handler(enter_agree, text_contains="agree", state=states.Purchase.Approval)
    dp.register_callback_query_handler(my_cart, text_contains="my_cart")
    dp.register_callback_query_handler(check_pay, text_contains="pre_finish_order")
    dp.register_callback_query_handler(pay_cash, text_contains="pay_cash", state=None)
    dp.register_message_handler(pay_cash_name, state=states.OrderItems.Name)
    dp.register_message_handler(pay_cash_phone, state=states.OrderItems.Phone)
    dp.register_message_handler(pay_cash_adress, state=states.OrderItems.Adress)
    dp.register_callback_query_handler(pay_card_cur, text='pay_card_cur')
    dp.register_message_handler(pay_card_name, state=states.OrderCard.Name_card)
    dp.register_message_handler(pay_card_phone, state=states.OrderCard.Phone_card)
    dp.register_message_handler(pay_card_adress, state=states.OrderCard.Adress_card)
    dp.register_shipping_query_handler(choose_shipping_city)
    dp.register_callback_query_handler(pay, text_contains="pay_card")
    dp.register_pre_checkout_query_handler(checkout)
