from config import TELEGRAM_TOKEN, REDIS_HOST, REDIS_PASSWORD, REDIS_USER

import redis.asyncio as redis

import asyncio

import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.redis import RedisStorage

from core.commands import register_base_commands_router
from core.db import create_the_engine, url_object, get_session_maker, BaseModel, proceed_schemas

from core.handlers import register_user_handlers_router
from core.scheduler.schedule import async_scheduler
from core.middlewares.is_admin import IsAdminMiddleware
from core.middlewares.mediagroup import AlbumMiddleware


async def starting_bot() -> None:
    """Start bot notify """
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    # Redis storage
    redis_ = redis.Redis(host=REDIS_HOST,
                         username=REDIS_USER or None,
                         password=REDIS_PASSWORD or None)
    storage = RedisStorage(redis=redis_)

    # Database
    postgres_url = url_object()  # create postgres url
    async_engine = create_the_engine(postgres_url)  # create engine
    session_mkr = get_session_maker(async_engine)  # create session_maker
    await proceed_schemas(async_engine, BaseModel.metadata)  # create tables of the db

    # start scheduler
    async_scheduler.start()

    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(storage=storage, session_maker=session_mkr, async_scheduler=async_scheduler)

    # middleware register
    dp.message.middleware.register(IsAdminMiddleware())
    dp.message.middleware.register(AlbumMiddleware())

    # filter only private messages and callbacks
    dp.message.filter(F.chat.type == 'private')
    dp.callback_query.filter(F.message.chat.type == 'private')

    # bot commands register
    register_base_commands_router(dp)

    # bot handlers register
    register_user_handlers_router(dp)
    # dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)

    # msgs = await objects_from_date('18.11.2023', session_mkr)
    # for ms in msgs:
    #     print(ms.post_date)
    await dp.start_polling(bot)


async def start_bot(bot: Bot) -> None:
    """Start bot notify"""
    pass


async def stop_bot(bot: Bot) -> None:
    """Stop bot notify"""
    pass


def main() -> None:
    """main function"""
    logger = logging.getLogger(__name__)
    try:
        asyncio.run(starting_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')


if __name__ == "__main__":
    main()
