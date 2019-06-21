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
    for x in resources.contents("emojimage.emoji"):
        if name in x:
            with resources.path("emojimage.emoji", x) as p:
                return Image.open(p).copy()
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
    h = image.histogram()

    r = h[0:256]
    g = h[256:256*2]
    b = h[256*2: 256*3]

    return (sum(i * w for i, w in enumerate(r)) // sum(r),
            sum(i * w for i, w in enumerate(g)) // sum(g),
            sum(i * w for i, w in enumerate(b)) // sum(b), 0)
