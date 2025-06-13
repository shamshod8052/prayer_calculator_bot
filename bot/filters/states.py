from aiogram.fsm.state import State, StatesGroup


class TestState(StatesGroup):
    STATE_NAME = State()

class InputState(StatesGroup):
    YEAR = State()
    DAY = State()
    QUESTION = State()
    QADA_NUMBER = State()
