from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def hours_keyboard(is_today: bool) -> InlineKeyboardMarkup:
    """
    hours keyboard
    :return: hour buttons
    """
    from_hour = 8
    if is_today:
        if datetime.now().hour < 8:
            from_hour = 8
        elif datetime.now().minute > 40 and datetime.now().hour < 23:
            from_hour = datetime.now().hour + 1
        else:
            from_hour = datetime.now().hour

    some_keyboard = InlineKeyboardBuilder()
    for hour in [str(hour) for hour in range(from_hour, 24)]:
        some_keyboard.button(text=f'{hour}:', callback_data=f'{hour}')
    some_keyboard.adjust(4)
    some_keyboard.row(InlineKeyboardButton(text='отмена', callback_data='отмена'))
    return some_keyboard.as_markup()


def hours_minutes_keyboard(is_today: bool, hour: str) -> InlineKeyboardMarkup:
    """
    hours:minutes keyboard hh:mm
    :return: quarter of hour buttons
    """
    some_keyboard = InlineKeyboardBuilder()
    minutes = ['00', '15', '30', '45']
    if not is_today or datetime.now().hour < int(hour):
        for minute in minutes:
            some_keyboard.button(text=f'{hour}:{minute}', callback_data=f'{hour}:{minute}')
    else:
        the_minute = datetime.now().minute // 15 + 1
        for minute in minutes[the_minute:]:
            some_keyboard.button(text=f'{hour}:{minute}', callback_data=f'{hour}:{minute}')

    some_keyboard.row(InlineKeyboardButton(text='отмена', callback_data='отмена'))
    some_keyboard.adjust(1)
    return some_keyboard.as_markup()


# def what_time_keyboard() -> InlineKeyboardMarkup:
#     some_keyboard = InlineKeyboardBuilder()
#
#     for hour in [str(hour) for hour in range(8, 23)]:
#         buttons = []
#         for minutes in ['00', '15', '30', '45']:
#             some_keyboard.button(text=f'{hour}:{minutes}', callback_data=f'{hour}:{minutes}')
#     some_keyboard.button(text='отмена', callback_data='отмена')
#     some_keyboard.adjust(4)
#     return some_keyboard.as_markup()