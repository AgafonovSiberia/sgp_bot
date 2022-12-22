from aiogram import types
from aiogram.dispatcher.router import Router
from .admin_panel import admin_panel_router
from .anniversary import anniversary_router
from .blocked_user import blocked_user_router
from .lottery import admin_lottery_router

admin_router = Router()
admin_router.include_router(admin_panel_router)
admin_router.include_router(admin_lottery_router)
admin_router.include_router(anniversary_router)
admin_router.include_router(blocked_user_router)


