from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..models.models import User
from ..common.context_manager import ContextManager

master_router = Router()

@master_router.message(
    CommandStart()
)
async def start_command_handler(
        message: Message,
        bot: Bot,
):
    user = await ContextManager.get(User)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Привет! Я - ассистент по подбору подходящей программы в ИТМО. Опиши свои компетенции",
    )