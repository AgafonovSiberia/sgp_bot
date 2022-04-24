import gspread
from bot.config_reader import config
from bot.models.member import MemberPydantic


async def format_update(member: MemberPydantic):
    return [member.user.user_id, member.user.user_name, member.user.user_nickname,
            member.user_status, member.user_passport.real_name, member.user_passport.position,
            member.user_passport.phone_number, member.from_user.user_id, member.from_user.user_name,
            member.from_user.user_nickname, member.invite_link, str(member.update_date)]


async def update_sheets(member_pydantic: MemberPydantic):
    event_data = await format_update(member_pydantic)
    client = gspread.service_account(filename=config.gsapi.key_path)
    g_sheet = client.open_by_key(config.gsapi.id)

    worksheet = g_sheet.get_worksheet(0)

    cell = worksheet.find(str(event_data[0]))

    if cell:
        print('Пользователь найден в ГуглТаб - обновляем')
        for x in range(1, 13):
            worksheet.update_cell(row=cell.row, col=x, value=event_data[x - 1])
    else:
        print("Пользователь не найден в ГуглТаб - пишу новую строку")
        worksheet.append_row(event_data)  # если такой записи нет - пишем строку в конец документа

