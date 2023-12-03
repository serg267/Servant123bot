from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def db_days_delete_keyboard(dates: list[list[str]]) -> InlineKeyboardMarkup:
    """
    post_delete keyboard
    :return: dates with quantity of the posts buttons
    """
    some_keyboard = InlineKeyboardBuilder()
    for text, date in dates:
        some_keyboard.button(text=text, callback_data=date)
    some_keyboard.row(InlineKeyboardButton(text='отмена', callback_data='отмена'))
    some_keyboard.adjust(1)
    return some_keyboard.as_markup()
