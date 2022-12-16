from aiogram import types
from aiogram.dispatcher.router import Router
from .main_panel import main_panel_router
from .anniversary import anniversary_router

admin_router = Router()
admin_router.include_router(main_panel_router)
admin_router.include_router(anniversary_router)


