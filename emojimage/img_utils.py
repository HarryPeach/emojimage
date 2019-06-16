from PIL import Image


def get_average_color(image_path):
    image = Image.open(image_path).convert("RGBA")
    resized_image = image.resize((1, 1))
    return resized_image.getpixel((0, 0))
