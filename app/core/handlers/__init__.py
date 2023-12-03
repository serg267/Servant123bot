__all__ = ['register_user_handlers_router']
from aiogram import Router

from .add_button_handlers import add_button_router
from .add_post_handler import call_router
from .forwarded_message_handlers import forwarded_router
from .callback_next_steps_handlers import call_steps_router
from .media_group_handlers import media_group_router
from .message_handlers import post_router
from .remove_post_handlers import remove_router


def register_user_handlers_router(router: Router) -> None:
    """all handlers router"""
    router.include_router(call_router)
    router.include_router(post_router)
    router.include_router(forwarded_router)
    router.include_router(media_group_router)
    router.include_router(call_steps_router)
    router.include_router(add_button_router)
    router.include_router(remove_router)


