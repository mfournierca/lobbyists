"""Download and unzip the raw data.

Usage:
    download_data.py [options]

Options:

    --help                        Show this help screen
"""
import logbook

from docopt import docopt
from urllib import urlretrieve
from zipfile import ZipFile

from src.constants import (
    SOURCE_DATA_ROOT,
    SOURCE_DATA_URL,
    SOURCE_DATA_ARCHIVE,
    SOURCE_DATA_DICTIONARY_FILE,
    SOURCE_DATA_DICTIONARY_URL
)


def download():
    logbook.info("downloading data set ... ")
    urlretrieve(SOURCE_DATA_URL, SOURCE_DATA_ARCHIVE)
    logbook.info("complete, unzipping data ... ")
    with ZipFile(SOURCE_DATA_ARCHIVE) as z:
        z.extractall(SOURCE_DATA_ROOT)
    logbook.info("downloading data dictionary ... ")
    urlretrieve(SOURCE_DATA_DICTIONARY_URL, SOURCE_DATA_DICTIONARY_FILE)
    logbook.info("complete")


if __name__ == "__main__":
    args = docopt(__doc__)
    download()
