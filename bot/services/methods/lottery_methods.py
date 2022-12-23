import typing
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, types

from bot.config_reader import config


async def ticket_factory(data_config: dict, user_id: int, bot: Bot):
        template = await get_template(data_config=data_config, bot=bot)
        ticket = ticket_draw(template=template, code=data_config.get("current_code"))
        file_id = await send_ticket(data_config=data_config, ticket=ticket, user_id=user_id, bot=bot)
        return file_id


async def send_ticket(data_config: dict, ticket: typing.BinaryIO, user_id: int, bot: Bot):

        msg = await bot.send_photo(chat_id=user_id, photo=types.BufferedInputFile(file=ticket, filename="ticket"),
                             caption=data_config.get("caption"))
        await bot.close()
        return msg.photo[-1].file_id


async def get_template(data_config: dict, bot: Bot):
        bot = Bot(config.bot_token, parse_mode="HTML")
        file = await bot.get_file(data_config.get("template_id"))
        template_image = await bot.download_file(file_path=file.file_path)
        await bot.close()
        return template_image


def ticket_draw(template, code: int):
        image = Image.open(template)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(r"bot/templates/Grus.ttf", size=160)
        text = f"ТВОЙ КОД: {code}"
        w, h = draw.textsize(text, font)
        left = (image.width - w) // 2
        draw.text((left, 250), text=text, font=font, fill=('#EBEFEF'))

        byte_io = BytesIO()
        image.save(byte_io, 'PNG')
        image = byte_io.getvalue()

        return image
