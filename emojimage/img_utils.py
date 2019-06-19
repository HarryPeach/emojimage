import logging
import os
from PIL import Image
from importlib import resources


def get_emoji_image(name):
    """Returns an image of an emoji, given its localized name. Returns None if emoji does not exist.

    Arguments:
        name {string} -- The localized name of the emoji

    Returns:
        PIL.Image -- The image of the emoji, None if emoji does not exist.
    """
    with resources.path("emojimage", "emoji") as p:
        for emoji_path in p.glob(name + ".*"):
            return Image.open(emoji_path)
        return None


def resize_image(image, scale):
    """Scale an image by a specific factor (Nearest Neighbour)

    Arguments:
        image {PIL.Image} -- The image object for PIL
        scale {int} -- The scale factor

    Returns:
        Image -- The scaled image
    """
    x, y = image.size
    return image.resize(tuple([scale * x, scale * y]))


def get_average_color(image):
    """Gets the average color of an image

    Arguments:
        image {PIL.Image} -- The image of which to calculate an average colour

    Returns:
        [tuple/int] -- The pixel value.
    """
    image = image.convert("RGBA")
    resized_image = image.resize((1, 1))
    return resized_image.getpixel((0, 0))
