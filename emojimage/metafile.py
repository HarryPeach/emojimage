import tempfile
import os
import csv
from importlib import resources
from .img_utils import get_average_color

METAFILE_NAME = "emojimage_metafile"


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
    with resources.path("emojimage", "emoji") as p:
        with open(get_metafile_path(), "w", newline='\n') as file:
            csvwriter = csv.writer(file, delimiter=',')
            for emoji_path in p.glob("*"):
                    r, g, b, a = get_average_color(emoji_path)
                    csvwriter.writerow([emoji_path.name, r, g, b])
