__all__ = ['register_base_commands_router', 'command_start', 'command_help']

from aiogram import Router
from aiogram.filters import Command

from .command_help import command_help
from .command_start import command_start


def register_base_commands_router(router: Router) -> None:
    """base commands router"""
    router.message.register(command_start, Command(commands=['start']))
    router.message.register(command_help, Command(commands=['help', 'команды']))
    # command_help not registered
