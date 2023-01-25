from typing import NamedTuple

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
class Extension(Enum):
    lottery = 1
    anniversary = 2
    @staticmethod
    def primary_config(name: str):
        return {"lottery": {"caption": None, "template_id": None},
                "anniversary": {},
                }.get(name, {})




class ValidInputError(NamedTuple):
    is_valid: bool
    error_text: str = ""
