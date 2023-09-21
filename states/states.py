from aiogram.fsm.state import State, StatesGroup


class EmailState(StatesGroup):
    subject = State()
    description = State()
    receiver = State()
    send_time = State()
