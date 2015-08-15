import sqlite3
from os.path import join
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Date
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

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d["com_date"] = datetime.strftime(d["com_date"], TIME_FORMAT)
        return d


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

