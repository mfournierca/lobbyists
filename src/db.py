import sqlite3
import pandas
import numpy
import Levenshtein

from os.path import join
from datetime import datetime
from sklearn import cluster

from sqlalchemy import Column, ForeignKey, Integer, String, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.constants import DATA_ROOT, TIME_FORMAT

SQLITE_DB_PATH = join(DATA_ROOT, "sqlite.db")

Base = declarative_base()


class DPOHCommDetailsView(Base):
    """A view containing details of each communication that a DPOH participated
    in.

    This is a view and not a table, it must be created by an SQL script and
    not by SQLAlchemy. Note that this class must be kept in sync with the
    script that creates the view.
    """
    __tablename__ = "dpoh_com_details"
    comlog_id = Column(Integer, primary_key=True, nullable=False)
    com_date = Column(Date, nullable=False)
    registrant_last_name = Column(String, nullable=False)
    registrant_first_name = Column(String, nullable=False)
    dpoh_last_name = Column(String, nullable=False)
    dpoh_first_name = Column(String, nullable=False)
    client_name = Column(String, nullable=False)
    subject_matter = Column(String, nullable=False)

    def com_date_str(self):
        return datetime.strftime(self.com_date, TIME_FORMAT)


class SubjectMatter(Base):
    """Subject of communications.

    Relates communication ids with the subject of the communication.
    """
    __tablename__ = "subject_matter"
    id = Column(Integer, primary_key=True, autoincrement=True)
    comlog_id = Column(Integer, nullable=False)
    subject_matter = Column(String, nullable=False)
    other_subject_matter = Column(String, nullable=True)


class CommunicationRegistrant(Base):
    """Lobbyist communication records.

    Relates communication ids to the lobbyist (registrant) that participated
    in the communication and some metedata.
    """
    __tablename__ = "communication_registrant"
    comlog_id = Column(Integer, nullable=False, primary_key=True)
    client_num = Column(
        Integer,
        ForeignKey("client.client_num"),
        nullable=False
    )
    registrant_num = Column(Integer, nullable=False)
    registrant_last_name = Column(String, nullable=False)
    registrant_first_name = Column(String, nullable=False)
    com_date = Column(Date, nullable=False)
    reg_type = Column(Integer, nullable=False)
    submission_date = Column(Date, nullable=False)
    posted_date = Column(Date, nullable=False)


class CommunicationDPOH(Base):
    """Pulic servant communication records.

    Relates communication ids to the public servant (DPOH) that participated
    as well as there current title and department.
    """
    __tablename__ = "communication_dpoh"
    comlog_id = Column(
        Integer,
        ForeignKey("communication_registrant.comlog_id"),
        ForeignKey("subject_matter.comlog_id"),
        primary_key=True,
        nullable=False
    )
    dpoh_last_name = Column(String, nullable=False, primary_key=True)
    dpoh_first_name = Column(String, nullable=False, primary_key=True)
    dpoh_title = Column(String, nullable=False)
    branch_unit = Column(String, nullable=True)
    other_institution = Column(String, nullable=True)
    institution = Column(String, nullable=True)


class Client(Base):
    """The client table contains metadata about lobbyist organizations."""
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_num = Column(Integer, nullable=False)
    client_name = Column(String, nullable=False)


ENGINE = create_engine("sqlite:///{0}".format(SQLITE_DB_PATH))
Base.metadata.create_all(ENGINE)


def make_sqlalchemy_session():
    return sessionmaker(bind=ENGINE)()


def get_raw_connection():
    return sqlite3.connect(SQLITE_DB_PATH)


def fix_mispelled_dpoh_names():
    names = _get_dpoh_name_freq()


def _get_dpoh_name_freq():
    session = make_sqlalchemy_session()
    query = session.query(
        CommunicationDPOH.dpoh_last_name,
        CommunicationDPOH.dpoh_first_name,
        func.count(CommunicationDPOH.comlog_id))
    query = query.group_by(
        CommunicationDPOH.dpoh_last_name,
        CommunicationDPOH.dpoh_first_name
    )
    query = query.order_by(
        CommunicationDPOH.dpoh_last_name,
        CommunicationDPOH.dpoh_first_name
    )
    return query.all()


def fix_mispelled_registrant_names():
    pass


def update_correct_names(df):
    pass


def find_correct_names(names):
    """Given a list of (lastname, firstname, frequency) tuples find the correct
    spelling of each name.

    We accomplish this in 2 steps:

    - Cluster the names so that mispellings are in the same cluster
    - Take the most frequent spelling from each cluster and consider it correct
    """

    df = pandas.DataFrame(names, columns=["lastname", "firstname", "count"])

    # distance will be measured off of full name
    df["name"] = df["lastname"] + df["firstname"]

    # remove non-ascii characters, sklearn crashes
    df["name"] = df["name"].apply(
        lambda x: "".join([i for i in x if 0 < ord(i) < 127])
    )

    # build distance matrix
    dist = _build_distance_matrix(df)

    # find labels
    dbscan = cluster.DBSCAN(eps=3, metric="precomputed", min_samples=1)
    labels = dbscan.fit_predict(dist)
    df["label"] = labels

    # find the index of the max count within each label
    correct = df.groupby("label")["count"].idxmax()

    # join with the original dataframe

    return df


def _build_distance_matrix(df, col="name"):
    dist = numpy.ndarray((len(df), len(df)))
    dist.fill(10000)
    width = 10
    for i, n in enumerate(df[col]):
        if i - width < 0:
            lower = 0
        else:
            lower = i - width

        if i + width > len(df[col]):
            upper = len(df[col])
        else:
            upper = i + width

        for j, m in enumerate(df[col][lower:upper]):
            pos = j + lower
            d = Levenshtein.distance(n, m)
            dist[i][pos] = d

    return dist
