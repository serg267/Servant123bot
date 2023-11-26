from datetime import datetime
from typing import Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async_scheduler = AsyncIOScheduler()


async def add_one_job(func: Callable, dtime: datetime, kwargs: dict) -> str:
    """adds job to a scheduler and returns job id"""
    job = async_scheduler.add_job(func, 'cron',
                                  year=dtime.year,
                                  month=dtime.month,
                                  day=dtime.day,
                                  hour=dtime.hour,
                                  minute=dtime.minute,
                                  kwargs=kwargs
                                  )
    return job.id


async def delete_job(job_id: str) -> None:
    """remove job from a scheduler"""
    if async_scheduler.get_job(job_id=job_id):
        async_scheduler.remove_job(job_id)
