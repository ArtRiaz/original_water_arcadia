from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def kb_menu():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton('🔖 Меню', callback_data="general_menu")
    ]])

    return ikb


def get_kb_menu():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton('💧 Наша компанія', callback_data="our_company"), InlineKeyboardButton('🕙 Режим роботи', callback_data="work")
    ], [
        InlineKeyboardButton('🏁 Зробити заказ', callback_data="do_order"), InlineKeyboardButton('🚰 Процес очистки', callback_data="cleaner")
    ], [
        InlineKeyboardButton('☎️ Контакти', callback_data="contact_menu"), InlineKeyboardButton('📲 Онлайн-консультація', callback_data="online")
    ]

    ])

    return ikb


def get_back():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton('↩️ Назад у головне  меню', callback_data="back_general_menu")
    ]])

    return ikb


"""Sertificate"""


def get_sertificate():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("🧾 Сертифікати", callback_data="sertif_menu")
    ], [
        InlineKeyboardButton("↩️ Назад у головне  меню", callback_data="back_general_menu")
    ]])

    return ikb
