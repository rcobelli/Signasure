import base64
from io import BytesIO
from PIL import ImageFont, Image, ImageDraw


def forge_name(name):
    res = {}
    for i in range(1, 16+1):
        font = ImageFont.truetype("sig-" + str(i) + ".ttf", 80)
        img = Image.new("RGB", (font.getsize(
            name)[0] + 80, 175), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((40, 40), name, (0, 0, 0), font=font)
        draw = ImageDraw.Draw(img)
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        image = buffer.getvalue()
        res[int(i-1)] = "data:image/jpeg;base64," + \
            str(base64.b64encode(image))[2:-1]
    return res
