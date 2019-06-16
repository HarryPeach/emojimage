import logging
import argparse
import os
from PIL import Image
from .metafile import generate_metafile, does_metafile_exist
from .log_manager import setup_custom_logger
from .img_utils import resize_image


def create_collage(path, image_scale=1, emoji_size=64):
    """Creates a collage of emojis from image data

    Arguments:
        path {string} -- The path to the original image

    Keyword Arguments:
        image_scale {int} -- The scale of the output image (default: {1})
        emoji_size {int} -- The size for each emoji to be (default: {64})
    """
    image = Image.open(path)
    print(image.size)
    if image_scale != 1:
        image = resize_image(image, image_scale)
    print(path)
    pass

if __name__ == "__main__":
    # Setup logger
    logger = setup_custom_logger("root")

    parser = argparse.ArgumentParser(description="convert an image into a collage of emojis")
    parser.add_argument("image_input", help="The image to convert")
    parser.add_argument("--force-metafile-generate", action="store_true",
                        help="Forces regeneration of the average-colour emoji metafile")

    args = parser.parse_args()

    # Setup emoji meta file
    if not does_metafile_exist() or args.force_metafile_generate:
        logger.info("Generating emoji metafile")
        generate_metafile()
    else:
        logger.debug("Emoji metafile already existed, and so was not created")

    # TODO implement arguments for width, height, and emoji size
    create_collage(args.image_input)
