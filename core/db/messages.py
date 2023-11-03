import datetime
from typing import Type, Union, List

from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from core.db import BaseModel


class Messages(BaseModel):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    post_type = Column(String, nullable=True)
    message_type = Column(String)
    message_json = Column(JSON)
    post_date = Column(TIMESTAMP, nullable=True)
    post_job_id = Column(String, nullable=True)
    telegram_msg_id = Column(JSON, nullable=True)
    delete_date = Column(TIMESTAMP, nullable=True)
    delete_job_id = Column(String, nullable=True)

    def __str__(self):
        return f"id {self.id}, post type {self.post_type}, post param: {self.post_date} - {self.delete_date}"


async def select_by_message_tgm_id(telegram_msg_id: int, session_maker: sessionmaker) -> None:
    """Take's Messages object from db by message_tgm_id"""
    async with session_maker() as session:
        stmt = select(Messages).where(Messages.telegram_msg_id == telegram_msg_id)
        session: AsyncSession
        obj = await session.execute(stmt)
        obj = obj.scalars().one()
        return obj


async def select_by_message_tgm_id_v2(telegram_msg_id: int, session_maker: sessionmaker) -> None:
    """Take's Messages object from db by message_tgm_id"""
    async with session_maker() as session:
        stmt = select(Messages).where(Messages.telegram_msg_id == telegram_msg_id)
        session: AsyncSession
        obj = await session.execute(stmt)
        obj = obj.scalars().one()
        return obj


# async def get_message(id: int, session_maker: async_sessionmaker) -> None:
#     """Take's Messages object from db by message_tgm_id"""
#     async with session_maker() as session:
#         stmt = get(Messages, id)
#         session: AsyncSession
#         obj = await session.execute(stmt)
#         obj = obj.scalars().one()
#         return obj


async def add_message(msg: Messages, session_maker: sessionmaker) -> Messages:
    """Add message to db"""
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            session.add(msg)  # add message
            await session.flush()  #
        await session.refresh(msg)
        obj = await session.get(Messages, msg.id)
        if not isinstance(obj, Messages):
            raise ValueError
    return obj


async def set_post_job_id(msg_id: int, post_job_id: str,  session_maker: sessionmaker) -> None:
    """Add post job id in db messages table object"""
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            obj = await session.get(Messages, msg_id)  # take message object
            obj.post_job_id = post_job_id  # add data and commit


async def set_delete_job_id(msg_id: int, delete_job_id: str, session_maker: sessionmaker) -> None:
    """Add delete job id in db messages table object"""
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            obj = await session.get(Messages, msg_id)  # take message object
            obj.delete_job_id = delete_job_id  # add data and commit


async def set_p_d_jobs_id(msg_id: int, post_job_id: str, delete_job_id: str,  session_maker: sessionmaker) -> None:
    """Add message with post and delete job id to db"""
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            obj = await session.get(Messages, msg_id)  # take message object
            obj.post_job_id = post_job_id
            obj.delete_job_id = delete_job_id


async def set_telegram_msg_id(db_message_id: int, telegram_msg_id: Union[int, List[int]],
                              session_maker: sessionmaker) -> None:
    """Add telegram_msg_id to message in db
    :rtype: object
    """
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            obj = await session.get(Messages, db_message_id)  # take message object
            obj.telegram_msg_id = telegram_msg_id  # add data and commit
