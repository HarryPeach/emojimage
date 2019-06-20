import logging
import argparse
import os
import random
from PIL import Image
from .metafile import (generate_metafile, does_metafile_exist, populate_emoji_dictionary, emoji_dictionary,
                       get_closest_colour)
from .log_manager import setup_custom_logger
from .img_utils import resize_image, get_emoji_image, get_average_color


def create_collage(path, image_scale=1, emoji_size=16):
    """Creates a collage of emojis from image data

    Arguments:
        path {string} -- The path to the original image

    Keyword Arguments:
        image_scale {int} -- The scale of the output image (default: {1})
        emoji_size {int} -- The size for each emoji to be (default: {16})
    """
    image = Image.open(path)

    # Populate the emoji dictionary if it is empty
    if not emoji_dictionary:
        populate_emoji_dictionary()

    # Resize the image if a scale is specified
    if image_scale != 1:
        image = resize_image(image, image_scale)

    # Unpack the image size
    width, height = image.size
    # How many emojis to use on the x axis
    emojis_x = width // emoji_size
    # How many emojis to use on the y axis
    emojis_y = height // emoji_size

    # The image to paste the emojis onto
    composite_image = Image.new("RGB", (width, height))
    # For every x emoji
    for x in range(0, emojis_x):
        for y in range(0, emojis_y):
            # Temporary image to crop and get average color
            temp_image = image.copy().crop((x * emoji_size,
                                            y * emoji_size,
                                            (x + 1) * emoji_size,
                                            (y + 1) * emoji_size))
            temp_avg = get_average_color(temp_image)

            offset = ((width//emojis_x) * x, (height//emojis_y) * y)
            emoji_image = get_emoji_image(random.choice(get_closest_colour(get_average_color(temp_image))))
            composite_image.paste(emoji_image.resize((emoji_size, emoji_size)), offset)

    # Save the final image
    composite_image.save("composite.png")


def main():
    # Setup logger
    logger = setup_custom_logger("root")

    # Setup argument parser
    parser = argparse.ArgumentParser(description="convert an image into a collage of emojis")
    parser.add_argument("image_input", help="The image to convert")
    parser.add_argument("--force-metafile-generate", action="store_true",
                        help="Forces regeneration of the average-colour emoji metafile")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable printing of debug logs")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    # Setup emoji meta file
    if not does_metafile_exist() or args.force_metafile_generate:
        generate_metafile()
    else:
        logger.debug("Emoji metafile already existed, and so was not created")

    # TODO implement arguments for width, height, and emoji size
    create_collage(args.image_input)


if __name__ == "__main__":
    main()
