import tempfile
import os
import csv
import logging
from PIL import Image
from importlib import resources
from .img_utils import get_average_color

METAFILE_NAME = "emojimage_metafile"
logger = logging.getLogger("root")

# A dictionary containing all emoji and color data
emoji_dictionary = dict()


def populate_emoji_dictionary():
    """Adds emoji data from metafile to the emoji dictionary
    """
    with open(get_metafile_path(), newline='\n') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            rgbval = tuple(row[-3:])
            emoji_dictionary.setdefault(rgbval, [])
            emoji_dictionary[rgbval].append(row[0])
    print(emoji_dictionary)


def get_metafile_path():
    """Gets the fully qualified path of the metafile

    Returns:
        string -- The metafile path
    """
    return os.path.join(tempfile.gettempdir(), METAFILE_NAME)


def does_metafile_exist():
    """Returns if the metafile already exists

    Returns:
        bool -- If the metafile already exists
    """
    return os.path.isfile(get_metafile_path())


def generate_metafile():
    """Generates a metafile of information about each emoji for easy use in the program
    """
    logger.info("Generating emoji metafile")
    logger.debug("Opening emoji resource folder")
    with resources.path("emojimage", "emoji") as p:
        logger.debug("Opening metafile")
        with open(get_metafile_path(), "w", newline='\n') as file:
            logger.debug("Writing emoji metadata")
            csvwriter = csv.writer(file, delimiter=',')
            for emoji_path in p.glob("*"):
                    image = Image.open(emoji_path)
                    r, g, b, a = get_average_color(image)
                    csvwriter.writerow([emoji_path.stem, r, g, b])
