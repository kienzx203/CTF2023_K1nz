from PIL import Image
from PIL import PngImagePlugin


def create_image():
    image = Image.new("RGBA", (690, 420), (255, 255, 255, 255))

    image.putpixel((412, 309), (52, 146, 235, 123))
    image.putpixel((12, 209), (42, 16, 125, 231))
    image.putpixel((264, 143), (122, 136, 25, 213))

    meta = PngImagePlugin.PngInfo()
    meta.add_text("Description", "jctf{not_the_flag}")
    meta.add_text("Title", "kool_pic")
    meta.add_text("Author", "anon")

    image.save("kool_pic.png", pnginfo=meta)


create_image()
