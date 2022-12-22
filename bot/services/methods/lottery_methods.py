from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


async def generate_ticket(img, code: int):
    image = Image.open(img)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r"bot/templates/Grus.ttf", size=160)
    text = f"ТВОЙ КОД: {code}"
    w, h = draw.textsize(text, font)
    left = (image.width - w) // 2
    draw.text((left, 250), text= text, font=font, fill=('#EBEFEF'))

    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    image = byte_io.getvalue()

    return image

