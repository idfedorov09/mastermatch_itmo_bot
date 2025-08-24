import functools
import asyncio
import logging
from collections import defaultdict

from ..common.context_manager import ContextManager
from ..models.models import User

logger = logging.getLogger(__name__)

class ReentrantAsyncLock:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._owner = None
        self._count = 0

    async def acquire(self):
        current = asyncio.current_task()
        if self._owner == current:
            self._count += 1
            return True
        await self._lock.acquire()
        self._owner = current
        self._count = 1
        return True

    def release(self):
        current = asyncio.current_task()
        if self._owner != current:
            raise RuntimeError("ReentrantAsyncLock: releasing unowned lock")
        self._count -= 1
        if self._count == 0:
            self._owner = None
            self._lock.release()

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.release()


_user_locks: defaultdict[str, ReentrantAsyncLock] = defaultdict(ReentrantAsyncLock)


def user_synchronized():
    """
    Декоратор, ставит лок на выполнение функции для конкретного пользователя.
    Блокирует одновременный вызов одной и той же функции/метода для одного user_id.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = await ContextManager.get(User)
            if current_user is not None:
                user_id = current_user.id
                lock = _user_locks[user_id]
            else:
                logger.warning("Can't find user to lock func execute - no session.")
                return await func(*args, **kwargs)

            async with lock:
                return await func(*args, **kwargs)

        return wrapper
    return decorator
