from aiogram.dispatcher.fsm.state import State, StatesGroup


class LeaveMember(StatesGroup):
    get_id_member = State()
    check_banned_member = State()


class LeftUserRegistration(StatesGroup):
    name_user = State()
    position_user = State()
    phone_number = State()
