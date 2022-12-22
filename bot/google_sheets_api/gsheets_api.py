import gspread
from bot.config_reader import config
from bot.models.member import MemberPydantic

from aiogram import Bot
from enum import Enum

class WORKSHEET(Enum):
    BASIC_IDX = 0
    LOTTERY_IDX = 1

async def format_update(member: MemberPydantic):
    return [member.user.user_id, member.user.user_name, member.user.user_nickname,
            member.user_status, member.user_passport.real_name, member.user_passport.position,
            member.user_passport.phone_number, member.from_user.user_id, member.from_user.user_name,
            member.from_user.user_nickname, member.invite_link, str(member.update_date)]


async def get_worksheet(worksheet: WORKSHEET):
    client = gspread.service_account_from_dict(info=config.GSAPI_SERVICE_KEY.dict())
    g_sheet = client.open_by_key(config.GSAPI_ID)
    worksheet = g_sheet.get_worksheet(worksheet.value)
    return worksheet


async def update_sheets(member_pydantic: MemberPydantic):
    event_data = await format_update(member_pydantic)
    worksheet = await get_worksheet(worksheet=WORKSHEET.BASIC_IDX)

    cell = worksheet.find(str(event_data[0]))

    if cell:
        for x in range(1, 13):
            worksheet.update_cell(row=cell.row, col=x, value=event_data[x - 1])
    else:
        worksheet.append_row(event_data)


async def check_unknown_user(user_id: int, bot_id: int) -> bool:
    """Вернёт True, если пользователь был добавлен в канал ботом и
    False, если пользователь был в канале раньше, чем добавили бота"""
    worksheet = await get_worksheet(WORKSHEET.BASIC_IDX)
    user_data = worksheet.row_values(worksheet.find(str(user_id)).row)
    if int(user_data[7]) != int(bot_id):
        return False
    return True


async def add_record_from_lottery(user_id: int, username: str, code: int):
    worksheet = await get_worksheet(WORKSHEET.LOTTERY_IDX)
    worksheet.append_row([user_id, username, code])









