from aiogram import types
from aiogram.dispatcher.router import Router
from .user_panel import user_panel_router
from .user_lottery import user_lottery_router

user_router = Router()
user_router.include_router(user_panel_router)
user_router.include_router(user_lottery_router)
