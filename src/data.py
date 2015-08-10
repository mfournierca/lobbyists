"""Download raw data and load it into the database.

Usage:

    data.py [options]

Options:

    --help  Show this help screen
"""
from urllib import urlretrieve
from zipfile import ZipFile
from os.path import join
from docopt import docopt
import logbook
import csv

from src.constants import DATA_ROOT
from src import db

SOURCE_DATA_URL = (
    "http://29040.vws.magma.ca/od-do_dl.php?f=Communications_OCL_CAL.zip"
)
SOURCE_DATA_DICTIONARY_URL = (
    "http://29040.vws.magma.ca/od-do_dl.php?f="
    "Communications_Dictionary_Dictionnaire_Communication.xlsx"
)
SOURCE_DATA_ARCHIVE = join(DATA_ROOT, "source.zip")
SOURCE_DATA_ROOT = join(DATA_ROOT, "source")
SOURCE_DATA_DICTIONARY_FILE = join(SOURCE_DATA_ROOT, "dictionary.xlsx")


def download():
    logbook.info("downloading data set ... ")
    urlretrieve(SOURCE_DATA_URL, SOURCE_DATA_ARCHIVE)
    logbook.info("complete, unzipping data ... ")
    with ZipFile(SOURCE_DATA_ARCHIVE) as z:
        z.extractall(SOURCE_DATA_ROOT)
    logbook.info("downloading data dictionary ... ")
    urlretrieve(SOURCE_DATA_DICTIONARY_URL, SOURCE_DATA_DICTIONARY_FILE)
    logbook.info("complete")


def load_data():
    pass


if __name__ == "__main__":
    args = docopt(__doc__)
    download()
