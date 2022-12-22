from aiogram.dispatcher.fsm.state import State, StatesGroup

from enum import Enum, unique

class LeaveMember(StatesGroup):
    get_id_member = State()
    check_banned_member = State()


class LeftUserRegistration(StatesGroup):
    name_user = State()
    position_user = State()
    phone_number = State()

class LotteryTemplate(StatesGroup):
    template = State()

class GetCongratulateData(StatesGroup):
    image = State()
    text = State()


@unique
class SlotStates(Enum):
    IS_EMPTY = 1
    IS_FULL = 2

@unique
class ExpansionModules(Enum):
    lottery = 1
    congratulation = 2
