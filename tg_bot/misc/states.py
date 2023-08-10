from aiogram.dispatcher.filters.state import StatesGroup, State


class Purchase(StatesGroup):
    EnterQuantity = State()
    Approval = State()


class NewItem(StatesGroup):
    Name = State()
    Photo = State()
    Description = State()
    Price = State()
    Confirm = State()


class OrderItems(StatesGroup):
    Name = State()
    Phone = State()
    Adress = State()
