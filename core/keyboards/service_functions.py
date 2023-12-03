from datetime import datetime

import pytz


def utc_to_mos_time(the_date: datetime) -> datetime:
    """change utc time to correct local Europe/Moscow time without timezone"""
    if the_date.tzname() != 'UTC':
        raise ValueError
    return the_date.astimezone(pytz.timezone('Europe/Moscow')).replace(tzinfo=None)


