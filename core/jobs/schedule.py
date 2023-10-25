from datetime import datetime
import asyncio
import os
from typing import Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def tick():
    print('Tick! The time is: %s' % datetime.now())


async_scheduler = AsyncIOScheduler()
# async_scheduler.add_job(tick, 'cron', year=2023, month=10, day=15, hour=19, minute=57)
# async_scheduler.add_job(tick, 'interval', seconds=3)


# async def main():
#     scheduler = AsyncIOScheduler()
#     scheduler.add_job(tick, 'cron', year=2023, month=10, day=15,  hour=19, minute=57)
#     scheduler.add_job(tick, 'interval', seconds=3)
#     scheduler.start()
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#     while True:
#         print('q')
#         await asyncio.sleep(10)
#
#
# if __name__ == '__main__':
#     # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
#     try:
#         asyncio.run(main())
#     except (KeyboardInterrupt, SystemExit):
#         pass

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
