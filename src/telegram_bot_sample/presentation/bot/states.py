from aiogram.fsm.state import State, StatesGroup


class MainMenuStatesGroup(StatesGroup):
    user = State()
    admin = State()
