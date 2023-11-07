import datetime

from sqlalchemy import Column, Integer, String, JSON, DATE, URL, MetaData, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from typing import Union


BaseModel = declarative_base()


def url_object() -> URL:
    """create url object with db connection variables"""
    url = URL.create(
        "postgresql+asyncpg",
        username="postgres",  # better to use env variables
        password="Nikola27",  # plain (unescaped) text
        host='localhost',  # better to use env variables
        port=5432,  # better to use env variables
        database="postgres",  # better to use env variables
    )
    return url


def create_the_engine(url: Union[URL, str]) -> AsyncEngine:
    """create connection to the db"""
    return create_async_engine(url=url, echo=False)


async def proceed_schemas(engine: AsyncEngine, metadata: MetaData) -> None:
    """create schemas in the db"""
    async with engine.begin() as conn:
        # await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)


def get_session_maker(_async_engine: AsyncEngine) -> async_sessionmaker:
    """to record and read data from the db"""
    return async_sessionmaker(_async_engine, class_=AsyncSession)







