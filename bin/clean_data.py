"""Preprocess and clean the data that has been loaded into the database.

Usage:
    clean_data.py [options]

Options:
    --help      Show this help page.
"""
import logbook

from docopt import docopt

from src.db import db
from src.data import clean


def _correct_mispelled_dpoh_names():
    names = db._get_dpoh_name_freq()
    df = clean.find_correct_names(names)


def run():
    pass


if __name__ == "__main__":
    args = docopt(__doc__)
    run()
