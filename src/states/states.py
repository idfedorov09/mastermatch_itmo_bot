from aiogram.fsm.state import StatesGroup, State

class RunState(StatesGroup):
    enter_comp = State()