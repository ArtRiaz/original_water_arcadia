from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""Contact"""


def ikb_contact():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton('👨🏼‍💻 www.arcadia.od.ua', url='https://www.arcadia.od.ua/')
    ], [
        InlineKeyboardButton('📍 Геолокація', callback_data='Геолокация')
    ], [
        InlineKeyboardButton('📞 +38(068)-555-77-12', callback_data='Вызов')
    ], [
        InlineKeyboardButton('↩️ Назад у головне  меню', callback_data="back_general_menu")
    ]])

    return ikb


"""Questions"""


def ikb_question():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton('💧 Очищення від домішок', callback_data="1")
    ], [InlineKeyboardButton("💧 Пом'якшення води ", callback_data="2")], [
        InlineKeyboardButton('💧 Видалення хлору', callback_data="3")
    ], [
        InlineKeyboardButton("💧 Додаткове очищення питної води", callback_data="4")
    ], [
        InlineKeyboardButton("💧 Знезараження води ", callback_data="5")
    ], [
        InlineKeyboardButton("💧 Покращення смаку", callback_data="6")
    ], [
        InlineKeyboardButton("💧 Ультрофиолетове очищення", callback_data="7")
    ], [
        InlineKeyboardButton("💧 Підготування та миття бутлів", callback_data="8")
    ], [
        InlineKeyboardButton('↩️ Назад у головне  меню', callback_data="back_general_menu")
    ]])

    return ikb


"""Back"""


def inline_questions_back():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("Назад", callback_data="cancel")
    ]])

    return ikb


"""Menu cart"""


def menu_cart():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("🚗 Оформити заказ", callback_data="pre_finish_order")
    ], [
        InlineKeyboardButton('↩️ Назад у головне  меню', callback_data="back_general_menu")
    ], [
        InlineKeyboardButton("❌ Очистити", callback_data="reset_cart")
    ]])

    return ikb


# Выбор способа оплаты
def pay_cash_or_card():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("💵 Оплатити готівкою", callback_data="pay_cash")
    ], [
        InlineKeyboardButton("💳 Оплатити через бота", callback_data="pay_card")
    ]])

    return ikb


# Меню админ панель

def menu_admin_panel():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("☑️ Додати товар", callback_data="add_item")
    ], [
        InlineKeyboardButton("❌ Видалити товар", callback_data="delete_item")
    ], [
        InlineKeyboardButton("📤 Розсилання", callback_data="send")
    ]])

    return ikb

# Назад в панель админа

def back_menu_admin_panel():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("↩️ Повернутись у админ панель", callback_data="back_admin_panel")
    ]])

    return ikb