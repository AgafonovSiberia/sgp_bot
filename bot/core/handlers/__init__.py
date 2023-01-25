from aiogram.dispatcher.router import Router
from bot.core.filters import BotStatusFilter
from .registration import registration_router, registration_exception_router
from .update import update_router, join_router, bot_status_router
from .user import user_router
from .admin import admin_router

core_router = Router()
core_router.include_router(admin_router)
core_router.include_router(user_router)
core_router.include_router(registration_router)
core_router.include_router(registration_exception_router)
core_router.include_router(update_router)
core_router.include_router(join_router)
core_router.include_router(bot_status_router)

core_router.message.filter(BotStatusFilter(bot_is_admin=True))
core_router.callback_query.filter(BotStatusFilter(bot_is_admin=True))





