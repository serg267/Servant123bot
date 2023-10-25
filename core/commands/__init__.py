__all__ = ['register_base_commands_router']

from aiogram import Router
from aiogram.filters import Command

from core.commands.command_start import command_start


def register_base_commands_router(router: Router) -> None:
    """base commands router"""
    router.message.register(command_start, Command(commands=['start']))
    # command_help not registered
