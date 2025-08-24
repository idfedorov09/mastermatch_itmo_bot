from typing import ClassVar, Any, Optional, TypeVar, Type
from aiogram.fsm.context import FSMContext
from pydantic import BaseModel

from ..common.context_manager import ContextManager
from ..common.user_sync import user_synchronized

T = TypeVar("T", bound="FSMDataClass")

class FSMDataClass(BaseModel):
    field_key: ClassVar[Optional[str]] = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if "field_key" not in kwargs:
            raise ValueError("field_key required")
        cls.field_key = kwargs.pop("field_key")
        super().__init_subclass__(**kwargs)

    @classmethod
    @user_synchronized()
    async def _get_state(cls) -> FSMContext:
        if not cls.field_key:
            raise ValueError("field_key is not set for the class")
        state: FSMContext = await ContextManager.get(FSMContext)
        if not state:
            raise RuntimeError("No FSMContext available")
        return state

    @user_synchronized()
    async def update(self) -> None:
        state: FSMContext = await self.__class__._get_state()
        await ContextManager.set(self)
        await state.update_data(**{self.field_key: self.model_dump()})

    @classmethod
    @user_synchronized()
    async def get(cls: Type[T]) -> Optional[T]:
        state: FSMContext = await cls._get_state()
        fsm_data = await state.get_data()
        data = fsm_data.get(cls.field_key)
        if data is not None:
            return cls(**data)
        return None

    @user_synchronized()
    async def delete(self) -> None:
        state: FSMContext = await self.__class__._get_state()
        data = await state.get_data()
        data.pop(self.field_key, None)
        await ContextManager.delete(self.__class__)
        await state.set_data(data)
