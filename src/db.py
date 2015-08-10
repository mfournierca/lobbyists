import sqlite3
from os.path import join
from src.constants import DATA_ROOT

SQLITE_DB_PATH = join(DATA_ROOT, "sqlite.db")
conn = sqlite3.connect(SQLITE_DB_PATH)


def create():
    """Create the tables and schema in the database"""
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE subject_matter (
            comlog_id INT,
            subject_matter VARCHAR,
            other_subject_matter VARCHAR,
            PRIMARY KEY (comlog_id)
        )"""
    )
