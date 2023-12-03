from datetime import date, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from static import DAYS_OF_WEEK


def date_keyboard() -> InlineKeyboardMarkup:
    """
    date keyboard
    :return: dates buttons
    """
    some_keyboard = InlineKeyboardBuilder()
    days_lasts_to_end_of_week = 7 - date.today().weekday()
    week = []
    # for _ in range(date.today().weekday()):
    #     some_keyboard.button(text='-', callback_data='*')
    for number in range(days_lasts_to_end_of_week):
        day = date.today() + timedelta(days=number)
        week.append(InlineKeyboardButton(text=DAYS_OF_WEEK[day.weekday()], callback_data=day.strftime('%d.%m.%Y')))
        #  some_keyboard.button(text=DAYS_OF_WEEK[day.weekday()], callback_data=day.strftime('%d.%m.%Y'))
    some_keyboard.row(*week)

    week = []
    for number in range(21):
        day = date.today() + timedelta(days=number + days_lasts_to_end_of_week)
        week.append(InlineKeyboardButton(text=day.strftime('%d.%m'), callback_data=day.strftime('%d.%m.%Y')))
        if (number + 1) % 7 == 0:
            some_keyboard.row(*week)
            week = []
    some_keyboard.row(InlineKeyboardButton(text='отмена', callback_data='отмена'))
    return some_keyboard.as_markup()
