"""Preprocess and clean the data that has been loaded into the database.

Usage:
    clean_data.py [options]

Options:
    --help      Show this help page.
"""
import logbook

from docopt import docopt

from src import db, data


def run():
    logbook.info("correcting names")
    db.util.fix_mispelled_dpoh_names()


if __name__ == "__main__":
    args = docopt(__doc__)
    run()
