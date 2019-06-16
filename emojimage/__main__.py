import logging
import argparse
from .metafile import generate_metafile, does_metafile_exist
from .log_manager import setup_custom_logger


def create_collage(path, width=512, height=512, emoji_size=64):
    """Creates a collage of emojis from image data

    Arguments:
        path {string} -- The path to the original image

    Keyword Arguments:
        width {int} -- The width of the output image (default: {512})
        height {int} -- The height of the output image (default: {512})
        emoji_size {int} -- The size for each emoji to be (default: {64})
    """
    # Calculate the emojis per row and column using floored division
    emojis_per_row = width // emoji_size
    emojies_per_column = height // emoji_size
    print(emojis_per_row)
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
