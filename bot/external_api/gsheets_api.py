import gspread
from bot.config_reader import config
from bot.misc.pydantic_models import MemberPydantic

from enum import Enum


class WORKSHEET(Enum):
    BASIC_IDX = 0
    LOTTERY_IDX = 1


def member_format_update(member: MemberPydantic):
    return [member.user.user_id, member.user.user_name,
            member.user.user_nickname, member.user_status,
            member.user_passport.real_name, member.user_passport.position,
            member.user_passport.phone_number, member.from_user.user_id,
            member.from_user.user_name, member.from_user.user_nickname,
            member.invite_link, str(member.update_date)]

def create_client():
    client = gspread.service_account_from_dict(
        info=config.GSAPI_SERVICE_KEY.dict())
    return client

def get_spreadsheet():
    client = create_client()
    spreadsheet = client.open_by_key(config.GSAPI_ID)
    return spreadsheet

def get_worksheet(worksheet: WORKSHEET):
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.get_worksheet(worksheet.value)
    return worksheet

