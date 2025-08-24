import json
import re
from typing import Any, Dict, Callable, Awaitable, Optional, TypeVar
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from aiogram.utils.serialization import deserialize_telegram_object_to_python

from ..common.context_manager import ContextManager
from ..models.models import User

T = TypeVar('T')


class DefaultMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data['bot']
        user_id = self._get_user_id_by_pattern(event)
        chat_id = self._get_chat_id_by_pattern(event)
        username = self._get_username_by_pattern(event)

        if chat_id is None:
            if user_id is None:
                return await handler(event, data)
            chat_id = user_id

        user = User(
            id=user_id,
            username=username,
        )

        await ContextManager.set(bot)
        await ContextManager.set(user)
        await ContextManager.set(data['state'])  # set FSM state

        result = await handler(event, data)

        return result

    @staticmethod
    def _get_user_id_by_pattern(event: TelegramObject) -> Optional[str]:
        event_json = _to_json(event)
        match = re.search(r'"from_user"\s*:\s*\{"id"\s*:\s*(\d+)', event_json)
        return match.group(1) if match else None

    @staticmethod
    def _get_username_by_pattern(event: TelegramObject) -> Optional[str]:
        event_json = _to_json(event)
        match = re.search(r'"from_user"\s*:\s*\{[^}]*"username"\s*:\s*"([^"]+)"', event_json)
        return match.group(1) if match else None

    @staticmethod
    def _get_chat_id_by_pattern(event: TelegramObject) -> Optional[str]:
        event_json = _to_json(event)
        match = re.search(r'"chat"\s*:\s*\{"id"\s*:\s*(-?\d+)', event_json)
        return match.group(1) if match else None


def _to_json(event: TelegramObject) -> str:
    return json.dumps(deserialize_telegram_object_to_python(event))
