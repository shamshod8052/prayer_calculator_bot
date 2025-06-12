from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    SELECT_MESSAGE_TYPE = State()
    SELECT_SEND_METHOD = State()
    SELECT_AUDIENCE = State()
    CONFIRM_SENDING = State()

class FilterState(StatesGroup):
    SETTING_FILTERS = State()
