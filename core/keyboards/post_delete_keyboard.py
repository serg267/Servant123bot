from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def string_days(days: str) -> str:
    match days:
        case '1':
            day = 'день'
        case ('2' | '3' | '4'):
            day = 'дня'
        case _:
            day = 'дней'
    return f'{days} {day}'


def delete_keyboard() -> InlineKeyboardMarkup:
    """
    post_delete keyboard
    :return: hour buttons
    """
    some_keyboard = InlineKeyboardBuilder()
    for day in [str(day) for day in range(1, 8)]:
        some_keyboard.button(text=string_days(day), callback_data=day)
    some_keyboard.row(InlineKeyboardButton(text='отмена', callback_data='отмена'))
    some_keyboard.adjust(1)
    return some_keyboard.as_markup()
