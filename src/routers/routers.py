from aiogram import Dispatcher

from ..middlewares.middlewares import DefaultMiddleware
from .master_route import master_router

def configure_routers(dp: Dispatcher):
    dp.update.outer_middleware(DefaultMiddleware())
    dp.include_routers(master_router)
