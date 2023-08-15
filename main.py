import asyncio
import logging

from config import load_config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewares.anti_time import Anti_time
# from tg_bot.fillters.admin import AdminFilter
# from tg_bot.handlers.admin import register_admin
from handlers.start import register_start
from handlers.our_company import register_handlers_about
from handlers.back import register_handler_back
from handlers.contact import register_handler_contact
from handlers.working_time import handler_calendar
from handlers.support import get_support
from handlers.questions import question_menu
from handlers.adminka.admin_panel import register_handler_create_items
from handlers.adminka.mailing import register_handler_mailing
from handlers.adminka.delete_item import register_delete_items
from misc.set_command_default import set_commands

logger = logging.getLogger(__name__)

def register_all_middleware(dp):
    dp.setup_middleware(Anti_time())


# def register_all_fillters(dp):
#     dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    # register_admin(dp)
    register_start(dp)
    register_handlers_about(dp)
    register_handler_back(dp)
    register_handler_contact(dp)
    handler_calendar(dp)
    get_support(dp)
    question_menu(dp)
    register_handler_create_items(dp)
    register_handler_mailing(dp)
    register_delete_items(dp)
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s'
    )

    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config  # доставать config из переменной bot, если в handler я хочу достать что то из Config
    # я делаю => bot.get("config")

    register_all_middleware(dp)
    # register_all_fillters(dp)
    register_all_handlers(dp)
    try:
        await dp.start_polling()
        await set_commands(bot=bot)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await dp.bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stop")
