from bot.misc.pydantic_models import MemberPydantic
from bot.service.workflow.worker import celery
from bot.external_api.gsheets_api import get_worksheet, WORKSHEET, member_format_update, get_spreadsheet
from bot.database.models import ChannelMember
from bot.misc.states import Extension

from gspread.exceptions import WorksheetNotFound, GSpreadException
from gspread.spreadsheet import Spreadsheet

WORKSHEET_ROWS_COUNT = 100
WORKSHEET_COLS_COUNT = 100

@celery.task(rate_limit="30/m")
def add_record_in_lottery_list(user: ChannelMember, code: int):
    worksheet = get_worksheet(WORKSHEET.LOTTERY_IDX)
    worksheet.append_row([code, user.user_id, user.user_tg_nickname, user.user_name, user.user_phone_number])


@celery.task(rate_limit="30/m")
def update_member_sheet(member_pydantic: MemberPydantic) -> None:
    event_data = member_format_update(member_pydantic)
    worksheet = get_worksheet(worksheet=WORKSHEET.BASIC_IDX)
    cell = worksheet.find(str(event_data[0]))

    if not cell:
        worksheet.append_row(event_data)
        return

    cell_range = worksheet.range(f'A{cell.row}:L{cell.row}')
    for cell, value in zip(cell_range, event_data):
        cell.value = str(value)
    worksheet.update_cells(cell_range)


@celery.task()
def lottery_list_reset() -> None:
    worksheet = get_worksheet(worksheet=WORKSHEET.LOTTERY_IDX)
    worksheet.clear()

@celery.task
def create_sheets_to_extensions() -> None:
    spreadsheet = get_spreadsheet()
    for ext in Extension:
        try:
            spreadsheet.get_worksheet(ext.value)
        except WorksheetNotFound:
            add_worksheet(spreadsheet=spreadsheet, ext=ext)


def add_worksheet(spreadsheet: Spreadsheet, ext: Extension) -> None:
    try:
        spreadsheet.add_worksheet(title=ext.name, index=ext.value,
                                  rows=WORKSHEET_ROWS_COUNT, cols=WORKSHEET_COLS_COUNT)
    except GSpreadException as e:
        #таблица с таким именем уже существует
        pass







