"""Download raw data and load it into the database.

Usage:

    data.py [options]

Options:

    --help      Show this help screen
    --download  Download data
    --load      Load data into the db
"""
from urllib import urlretrieve
from zipfile import ZipFile
from os.path import join
from docopt import docopt
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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

STRPTIME_FORMAT = "%Y-%m-%d"


def download():
    logbook.info("downloading data set ... ")
    urlretrieve(SOURCE_DATA_URL, SOURCE_DATA_ARCHIVE)
    logbook.info("complete, unzipping data ... ")
    with ZipFile(SOURCE_DATA_ARCHIVE) as z:
        z.extractall(SOURCE_DATA_ROOT)
    logbook.info("downloading data dictionary ... ")
    urlretrieve(SOURCE_DATA_DICTIONARY_URL, SOURCE_DATA_DICTIONARY_FILE)
    logbook.info("complete")


def load_all():
    session = sessionmaker(bind=db.engine)()
    load_subject_matter(session)
    load_communication_registrant(session)
    load_communication_dpoh(session)
    load_client(session)


def load_client(session):
    with open(join(SOURCE_DATA_ROOT, "CLIENT_NMExport.csv")) as w:
        r = csv.reader(w)
        header = r.next()
        b = 0
        for row in r:
            row = [unicode(i, errors="replace") for i in row[:2]]
            session.add(db.Client(
                client_num=row[0],
                client_name=row[1]
            ))
            b += 1
            if b % 10000 == 0:
                session.commit()
        session.commit()


def load_communication_registrant(session):
    with open(
        join(SOURCE_DATA_ROOT, "Communication_PrimaryExport.csv")
    ) as w:
        r = csv.reader(w)
        header = r.next()
        b = 0
        for row in r:
            row = [i.decode("utf-8") for i in row]
            session.add(db.CommunicationRegistrant(
                comlog_id=row[0],
                client_num=row[1],
                registrant_num=row[2],
                registrant_last_name=row[3],
                registrant_first_name=row[4],
                com_date=datetime.strptime(row[5], STRPTIME_FORMAT),
                reg_type=row[6],
                submission_date=datetime.strptime(row[7], STRPTIME_FORMAT),
                posted_date=datetime.strptime(row[8], STRPTIME_FORMAT)
            ))
            b += 1
            if b % 10000 == 0:
                session.commit()
        session.commit()


def load_communication_dpoh(session):
    with open(
        join(SOURCE_DATA_ROOT, "Communication_DPOHExport.csv")
    ) as w:
        r = csv.reader(w)
        header = r.next()
        b = 0
        for row in r:
            row = [i.decode("utf-8") for i in row]
            session.add(db.CommunicationDPOH(
                comlog_id=row[0],
                dpoh_last_name=row[1],
                dpoh_first_name=row[2],
                dpoh_title=row[3],
                branch_unit=row[4],
                other_institution=row[5],
                institution=row[6]
            ))
            b += 1
            if b % 10000 == 0:
                session.commit()
        session.commit()


def load_subject_matter(session):
    with open(
        join(SOURCE_DATA_ROOT, "Communication_SubjectMattersExport.csv")
    ) as w:
        r = csv.reader(w)
        header = r.next()
        b = 0
        for row in r:
            row = [i.decode("utf-8") for i in row]
            session.add(db.SubjectMatter(
                comlog_id=row[0],
                subject_matter=row[1],
                other_subject_matter=row[1]
            ))
            b += 1
            if b % 10000 == 0:
                session.commit()
        session.commit()


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--download"]:
        download()
    if args["--load"]:
        load_all()
