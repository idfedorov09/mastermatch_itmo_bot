from contextvars import ContextVar
from contextlib import asynccontextmanager
from typing import Dict, Type, Any, TypeVar, Optional, cast

T = TypeVar("T")


class ContextManager:

    _request_context: ContextVar[Dict[Type[Any], Any]] = ContextVar(
        "request_context",
        default={}
    )

    @classmethod
    async def set(cls, obj: T) -> None:
        old_ctx = cls._request_context.get()
        new_ctx = dict(old_ctx)
        new_ctx[obj.__class__] = obj
        cls._request_context.set(new_ctx)

    @classmethod
    async def get(cls, obj_type: Type[T]) -> Optional[T]:
        return cast(Optional[T], cls._request_context.get().get(obj_type))

    @classmethod
    async def has(cls, obj_type: Type[Any]) -> bool:
        return obj_type in cls._request_context.get()

    @classmethod
    async def clear(cls) -> None:
        cls._request_context.set({})

    @classmethod
    async def get_all(cls) -> Dict[Type[Any], Any]:
        """
        Возвращает копию всего текущего словаря контекста (для отладки).
        """
        return dict(cls._request_context.get())

    @classmethod
    @asynccontextmanager
    async def temp_set(cls, obj: T):
        old_ctx = cls._request_context.get()
        new_ctx = dict(old_ctx)
        new_ctx[obj.__class__] = obj
        cls._request_context.set(new_ctx)

        try:
            yield
        finally:
            cls._request_context.set(old_ctx)

    @classmethod
    @asynccontextmanager
    async def isolate_context(cls, new_value: Optional[Dict[Type[Any], Any]] = None):
        old_ctx = cls._request_context.get()
        if new_value is None:
            new_value = dict(old_ctx)
        cls._request_context.set(new_value)
        try:
            yield
        finally:
            cls._request_context.set(old_ctx)

    @classmethod
    async def delete(cls, obj_type: T) -> None:
        old_ctx = cls._request_context.get()
        new_ctx = dict(old_ctx)
        new_ctx.pop(obj_type, None)
        cls._request_context.set(new_ctx)