import json

from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN, ADMINCHAT
import asyncio
import logging

from core.commands import register_base_commands_router
from core.db.database import create_the_engine, url_object, get_session_maker, BaseModel, proceed_schemas
from core.db.messages import select_by_message_tgm_id_v2

from core.handlers import register_user_handlers_router
from core.jobs.schedule import async_scheduler
from core.middlewares.is_admin import IsAdminMiddleware
from core.middlewares.mediagroup import AlbumMiddleware
from core.models.States import storage


async def start_bot(bot: Bot) -> None:
    """Start bot notify """
    pass


async def stop_bot(bot: Bot) -> None:
    """Stop bot notify"""
    pass


async def main() -> None:
    """launch bot"""
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    # Database
    postgres_url = url_object()                                          # create postgres url
    async_engine = create_the_engine(postgres_url)                       # create engine
    session_mkr = get_session_maker(async_engine)                        # create session_maker
    await proceed_schemas(async_engine, BaseModel.metadata)              # create tables of the db

    # start jobs
    async_scheduler.start()

    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(storage=storage, session_maker=session_mkr, async_scheduler=async_scheduler)
    # middleware register
    dp.message.middleware.register(IsAdminMiddleware())
    dp.message.middleware.register(AlbumMiddleware())

    # bot commands register
    register_base_commands_router(dp)
    # bot handlers register
    register_user_handlers_router(dp)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
