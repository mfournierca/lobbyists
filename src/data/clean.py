import logbook
import re

import pandas as pd
import Levenshtein

from sqlalchemy import update
from sqlalchemy import exc as sqlalchemy_exceptions

from src.db import db, util
from src.data import correct_names

PUNCTUATION = [
    ".",
    ","
]

REPLACE = [
    "the",
    "right",
    "rt",
    "hon",
    "honorable",
    "honourable",
    "mp",
    "pc"
]

SUB = ["^" + r + "\s+" for r in REPLACE]
SUB += ["\s+" + r + "\s+" for r in REPLACE]


def clean_name(name):
    """Clean the provided name. Capitalize properly, remove punctuation,
    titles and pronouns. """

    name = name.lower()
    name = name.strip()
    for p in PUNCTUATION:
        name = name.replace(p, "")
    for i in SUB:
        name = re.sub(i, "", name)
    name = name.title()
    return name


def clean_last_and_first_name(lastname, firstname):
    return clean_name(lastname), clean_name(firstname)


def fix_mispelled_dpoh_names():
    """Find and fix mispellings in DPOH names in the db"""

    logbook.debug("computing correct names")
    names = util.get_dpoh_name_freq()
    df = correct_names.find_correct_names(names)

    conn = db.get_sqlalchemy_connection()
    trans = conn.begin()

    counter = 0
    logbook.debug("updating db")
    for row in df.iterrows():
        row = row[1]

        firstname = row["firstname"]
        lastname = row["lastname"]
        correct_firstname = row["correct_firstname"]
        correct_lastname = row["correct_lastname"]

        stmt = update(db.CommunicationDPOH.__table__).where(
            db.CommunicationDPOH.dpoh_first_name == firstname
        ).where(
            db.CommunicationDPOH.dpoh_last_name == lastname
        ).values(
            dpoh_first_name=correct_firstname,
            dpoh_last_name=correct_lastname
        )

        try:
            # misspellings can cause collisions
            trans.connection.execute(stmt)
        except sqlalchemy_exceptions.IntegrityError as e:
            logbook.error(e)
            continue

        counter += 1
        if counter % 250 == 0:
            trans.commit()
            trans.close()
            trans = conn.begin()
            logbook.debug("committed {0} changes".format(counter))

    trans.commit()
    trans.close()
    logbook.debug("committed {0} changes".format(counter))


def fix_mispelled_registrant_names():
    pass


def update_correct_names(df):
    pass

