import logging

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class Anti_time(BaseMiddleware):
    async def on_pre_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        await cq.answer()
