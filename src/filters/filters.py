from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class EmptyStateFilter(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        return current_state is None or current_state.strip() == ''