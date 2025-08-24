import os

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config.config_models import bot_config
from .config.logger_config import configure_logging as conf_logging
from .routers import configure_routers

async def main():
    await configure_logging()
    await start_polling()


async def configure_logging():
    _log_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(_log_dir):
        os.makedirs(_log_dir)
    conf_logging(_log_dir)
    pass

async def start_polling():
    bot = Bot(
        token=bot_config.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    configure_routers(dp)
    await dp.start_polling(bot)
