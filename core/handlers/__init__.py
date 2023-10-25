__all__ = ['register_user_handlers_router']
from aiogram import Router

from .forwarded_message_handlers import forwarded_post_router
from .callback_next_steps_handlers import post_msg_next_steps_router
from .resend_media_group_to_admins import media_group_router
from .message_handlers import post_router


def register_user_handlers_router(router: Router) -> None:
    """forward, resend, and reply handlers router"""
    router.include_router(post_router)
    router.include_router(forwarded_post_router)
    router.include_router(media_group_router)
    router.include_router(post_msg_next_steps_router)

