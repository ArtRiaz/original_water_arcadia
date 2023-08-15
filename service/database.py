from aiogram import types
from gino import Gino
from sqlalchemy import (Column, Integer, BigInteger, String,
                        Sequence, TIMESTAMP)
from sqlalchemy import sql
# from gino.schema import GinoSchemaVisitor
from config import load_config, POSTGRES_URL

db = Gino()

config = load_config()


# Документация
# http://gino.fantix.pro/en/latest/tutorials/tutorial.html

# class BaseModel(db.Model):
#     __abstract__ = True
#
#     def __str__(self):
#         model = self.__class__.__name__
#         table: sa.Table = sa.intersect(self.__class__)
#         primary_key_columns: List[sa.Column] = table.primary_key.columns
#         values = {
#             column.name: getattr(self, self._column_name_map[column.name])
#             for column in primary_key_columns
#         }
#         values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
#         return f"<{model} {values_str}>"


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(BigInteger)
    full_name = Column(String(100))
    username = Column(String(50))
    query: sql.Select

    def __repr__(self):
        return "<User(id='{}', fullname='{}', username='{}')>".format(
            self.id, self.full_name, self.username)


print(User())


class Item(db.Model):
    __tablename__ = 'items'
    query: sql.Select

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    photo = Column(String(350))
    description = Column(String(250))
    price = Column(Integer)  # Цена в копейках (потом делим на 100)


def __repr__(self):
    return "<Item(id='{}', name='{}', photo='{}', description='{}' price='{}')>".format(
        self.id, self.name, self.photo, self.description, self.price)


class Purchase(db.Model):
    __tablename__ = 'purchases'
    query: sql.Select

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    buyer = Column(BigInteger)
    item_id = Column(Integer)
    name = Column(String)
    amount = Column(Integer)  # Цена в копейках (потом делим на 100)
    quantity = Column(Integer)
    purchase_time = Column(TIMESTAMP)


class DBCommands:

    async def get_user(self, user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def add_new_user(self):
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name
        await new_user.create()
        return new_user

    async def count_users(self) -> int:
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def get_all_user_ids(self):
        users = await User.query.gino.all()  # Получаем всех пользователей из таблицы
        user_ids = [user.user_id for user in users]
        return user_ids

    async def show_items(self):
        await db.set_bind(POSTGRES_URL)
        items = await Item.query.gino.all()

        return items

    async def show_cart(self, user_id):
        purchases = await Purchase.query.where(Purchase.buyer == user_id).gino.all()

        return purchases

    async def empty_cart(self, user_id):
        purchases = await Purchase.delete.where(Purchase.buyer == user_id).gino.status()

        return purchases

    async def del_item(self, data):
        purchases = await Item.delete.where(Item.name == data).gino.status()

        return purchases


async def create_db():
    await db.set_bind(POSTGRES_URL)

    # Create tables
    # db.gino = GinoSchemaVisitor

    #    await db.gino.drop_all()
    await db.gino.create_all()
