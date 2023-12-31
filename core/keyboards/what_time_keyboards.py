from datetime import datetime

import pytz

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.keyboards import utc_to_mos_time


def hours_keyboard(is_today: bool) -> InlineKeyboardMarkup:
    """
    hours keyboard
    :return: hour buttons
    """
    from_hour = 8
    if is_today:
        if utc_to_mos_time(datetime.now(pytz.utc)).hour < 8:
            from_hour = 8
        elif utc_to_mos_time(datetime.now(pytz.utc)).minute > 40 and utc_to_mos_time(datetime.now(pytz.utc)).hour < 23:
            from_hour = utc_to_mos_time(datetime.now(pytz.utc)).hour + 1
        else:
            from_hour = utc_to_mos_time(datetime.now(pytz.utc)).hour

    some_keyboard = InlineKeyboardBuilder()
    for hour in [str(hour) for hour in range(from_hour, 24)]:
        some_keyboard.button(text=f'{hour}:', callback_data=f'{hour}')
    some_keyboard.adjust(4)
    some_keyboard.row(InlineKeyboardButton(text='отмена', callback_data='cancel'))
    return some_keyboard.as_markup()


def hours_minutes_keyboard(is_today: bool, hour: str) -> InlineKeyboardMarkup:
    """
    hours:minutes keyboard hh:mm
    :return: quarter of hour buttons
    """
    some_keyboard = InlineKeyboardBuilder()
    minutes = ['00', '15', '30', '45']

    if not is_today or utc_to_mos_time(datetime.now(pytz.utc)).hour < int(hour):
        for minute in minutes:
            some_keyboard.button(text=f'{hour}:{minute}', callback_data=f'{hour}:{minute}')
    else:
        the_minute = utc_to_mos_time(datetime.now(pytz.utc)).minute // 15 + 1
        for minute in minutes[the_minute:]:
            some_keyboard.button(text=f'{hour}:{minute}', callback_data=f'{hour}:{minute}')

    some_keyboard.row(InlineKeyboardButton(text='отмена', callback_data='cancel'))
    some_keyboard.adjust(1)
    return some_keyboard.as_markup()
