"""Download raw data and load it into the database.

Usage:
    data.py --help
    data.py (--download|--load) [options]

Options:

    --help                        Show this help screen
    --download                    Download data
    --load                        Load data into the db
    --commit-interval=<interval>  Number of rows to commit at a time
                                  [default: 10000]
"""

from urllib import urlretrieve
from zipfile import ZipFile
from os.path import join
from docopt import docopt
from datetime import datetime

import logbook
import csv

from src.constants import DATA_ROOT, SQL_SCRIPTS_DIR, TIME_FORMAT
from src import db
from src import common

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


def load_all(commit_interval=10000):
    session = db.make_sqlalchemy_session()
    load_subject_matter(session, commit_interval=commit_interval)
    load_communication_registrant(session, commit_interval=commit_interval)
    load_communication_dpoh(session, commit_interval=commit_interval)
    load_client(session, commit_interval=commit_interval)
    run_sql_scripts()


def run_sql_scripts():
    logbook.info("running sql scripts")
    scripts = [
        join(SQL_SCRIPTS_DIR, "dpoh_com_details_view.sql"),
        join(SQL_SCRIPTS_DIR, "create_indices.sql")
    ]
    conn = db.get_raw_connection()
    for script in scripts:
        logbook.debug("running {0}".format(script))
        sql = open(script, "r")
        conn.executescript("".join(sql.readlines()))


def _load(session, csvfile, row_creator, commit_interval=10000):
    with open(csvfile) as w:
        r = csv.reader(w)
        header = r.next()
        b = 0
        for row in r:
            row = [unicode(i, errors="replace") for i in row if i is not None]
            session.merge(row_creator(row))
            b += 1
            if b % commit_interval == 0:
                session.commit()
                logbook.debug("committed {0} rows".format(b))
        session.commit()
        logbook.debug("committed {0} rows".format(b))


def load_client(session, commit_interval=10000):
    logbook.info("loading client data")

    row_creator = lambda row: db.Client(
        client_num=row[0], client_name=row[1]
    )

    _load(
        session,
        join(SOURCE_DATA_ROOT, "CLIENT_NMExport.csv"),
        row_creator,
        commit_interval=commit_interval
    )


def _create_communication_registrant(row):
    lastname, firstname = common.clean_last_and_first_name(row[3], row[4])
    return db.CommunicationRegistrant(
        comlog_id=row[0],
        client_num=row[1],
        registrant_num=row[2],
        registrant_last_name=lastname,
        registrant_first_name=firstname,
        com_date=datetime.strptime(row[5], TIME_FORMAT),
        reg_type=row[6],
        submission_date=datetime.strptime(row[7], TIME_FORMAT),
        posted_date=datetime.strptime(row[8], TIME_FORMAT)
    )


def load_communication_registrant(session, commit_interval=10000):
    logbook.info("loading communication registrant data")
    _load(
        session,
        join(SOURCE_DATA_ROOT, "Communication_PrimaryExport.csv"),
        _create_communication_registrant,
        commit_interval=commit_interval
    )


def _create_communication_dpoh(row):
    lastname, firstname = common.clean_last_and_first_name(row[1], row[2])
    return db.CommunicationDPOH(
        comlog_id=row[0],
        dpoh_last_name=lastname,
        dpoh_first_name=firstname,
        dpoh_title=row[3],
        branch_unit=row[4],
        other_institution=row[5],
        institution=row[6]
    )


def load_communication_dpoh(session, commit_interval=10000):
    logbook.info("loading dpoh communication data")
    _load(
        session,
        join(SOURCE_DATA_ROOT, "Communication_DPOHExport.csv"),
        _create_communication_dpoh,
        commit_interval=commit_interval
    )


def load_subject_matter(session, commit_interval=10000):
    logbook.info("loading subject matter data")

    row_creator = lambda row: db.SubjectMatter(
        comlog_id=row[0],
        subject_matter=row[1],
        other_subject_matter=row[1]
    )

    _load(
        session,
        join(SOURCE_DATA_ROOT, "Communication_SubjectMattersExport.csv"),
        row_creator,
        commit_interval=commit_interval
    )


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--download"]:
        download()
    if args["--load"]:
        load_all(commit_interval=int(args["--commit-interval"]))
