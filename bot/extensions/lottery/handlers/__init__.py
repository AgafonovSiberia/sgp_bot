from aiogram.dispatcher.router import Router
from .user import user_lottery_router
from .admin import admin_lottery_router

extension_lottery_router = Router()
extension_lottery_router.include_router(user_lottery_router)
extension_lottery_router.include_router(admin_lottery_router)

