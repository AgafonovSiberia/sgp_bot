from aiogram import types
from aiogram.dispatcher.router import Router
from .bot_status_update import bot_status_router
from .update_member import update_router
from .join_member import join_router

member_update_router = Router()
member_update_router.include_router(bot_status_router)
member_update_router.include_router(update_router)
member_update_router.include_router(join_router)
