import logging
from .metafile import generate_metafile, does_metafile_exist
from .log_manager import setup_custom_logger

if __name__ == "__main__":
    logger = setup_custom_logger("root")

    # Setup emoji meta file
    if not does_metafile_exist():
        generate_metafile()
    else:
        logger.debug("Emoji metafile already existed, and so was not created")
