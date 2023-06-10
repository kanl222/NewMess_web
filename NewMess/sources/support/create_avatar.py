import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
from base64 import b64encode
from io import BytesIO

font_path = os.path.abspath("sources/font/arialmt.ttf")
font = ImageFont.truetype(font_path, 16)

bg_color_array = np.zeros((48, 48, 3), dtype=np.uint8)

def generate_avatar(username, font_color=(240, 240, 240), return_PNG_bytes=False):
    size = 48
    text = username[0].upper()
    
    background_color = tuple(random.randint(0, 240) for _ in range(3))
    
    bg_color_array[:, :, :] = background_color
    image = Image.fromarray(bg_color_array)
    
    draw = ImageDraw.Draw(image)
    text_size = draw.textsize(text, font=font)
    position = ((size - text_size[0]) // 2, (size - text_size[1]) // 2)
    
    fill = (font_color,) * 3 if isinstance(font_color, int) else font_color
    draw.text(position, text, fill=fill, font=font)
    
    if return_PNG_bytes:
        with BytesIO() as output:
            image.save(output, format="PNG", optimize=True, quality=95)
            output.seek(0)
            return b64encode(output.getvalue()).decode('utf-8')
    else:
        return image
