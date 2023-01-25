from bot.service.workflow.worker import celery
import typing
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, types, exceptions
import asyncio
from bot.config_reader import config




@celery.task()
def generate_lottery_ticket(data_config: dict, user_id: int):
        result = asyncio.run(ticket_factory(data_config=data_config, user_id=user_id))
        return result




async def ticket_factory(data_config: dict, user_id: int,):
        bot = Bot(token=config.bot_token, parse_mode="HTML")
        template = await get_template(data_config=data_config, bot=bot)
        ticket = ticket_draw(template=template, code=data_config.get("current_code"))
        file_id = await send_ticket(data_config=data_config, ticket=ticket, user_id=user_id, bot=bot)
        await bot.session.close()
        return file_id


async def send_ticket(data_config: dict, ticket: typing.BinaryIO, user_id: int, bot: Bot):
        try:
                msg = await bot.send_photo(chat_id=user_id,caption=data_config.get("caption"),
                                           photo=types.BufferedInputFile(file=ticket, filename="ticket"))
        except exceptions.TelegramRetryAfter:
                asyncio.sleep(5)
                return send_ticket(data_config=data_config, ticket=ticket, user_id=user_id, bot=bot)
        else:
                return msg.photo[-1].file_id




async def get_template(data_config: dict, bot: Bot):
        file = await bot.get_file(data_config.get("template_id"))
        template_image = await bot.download_file(file_path=file.file_path)
        return template_image


def ticket_draw(template: BytesIO, code: int) -> BytesIO:
        """
        Отрисовываем билет на участие в розыгрыше.
        :param template: шаблон/фон билета.
        :param code: номер билета пользователя.
        :return:
        """
        image = Image.open(template)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(r"bot/templates/fonts/basic_font.ttf", size=120)
        text = f"ТВОЙ КОД: {code}"
        w, h = draw.textsize(text, font)
        left = (image.width - w) // 2
        draw.text((left, 230), text=text, font=font, fill=('#EBEFEF'))

        byte_io = BytesIO()
        image.save(byte_io, 'PNG')
        image = byte_io.getvalue()

        return image
