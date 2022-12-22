from aiogram import types
from aiogram.dispatcher.router import Router
from .exceptions import exceptions_private_router
from .registration import registration_private_router

registration_router = Router()
registration_router.include_router(registration_private_router)
registration_router.include_router(exceptions_private_router)
