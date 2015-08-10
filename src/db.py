from os.path import join
from src.constants import DATA_ROOT

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

SQLITE_DB_PATH = join(DATA_ROOT, "sqlite.db")

Base = declarative_base()


class SubjectMatter(Base):
    __tablename__ = "subject_matter"
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    comlog_id = Column(Integer, nullable=False)
    subject_matter = Column(String, nullable=False)
    other_subject_matter = Column(String, nullable=True)


class CommunicationRegistrant(Base):
    __tablename__ = "communication_registrant"
    comlog_id = Column(Integer, nullable=False, primary_key=True)
    client_num = Column(Integer, nullable=False)
    registrant_num = Column(Integer, nullable=False)
    registrant_last_name = Column(String, nullable=False)
    registrant_first_name = Column(String, nullable=False)
    com_date = Column(Date, nullable=False)
    reg_type = Column(Integer, nullable=False)
    submission_date = Column(Date, nullable=False)
    posted_date = Column(Date, nullable=False)


class CommunicationDPOH(Base):
    __tablename__ = "communication_dpoh"
    comlog_id = Column(Integer, nullable=False, primary_key=True)
    dpoh_last_name = Column(String, nullable=False)
    dpoh_first_name = Column(String, nullable=False)
    dpoh_title = Column(String, nullable=False)
    branch_unit = Column(String, nullable=True)
    other_institution = Column(String, nullable=True)
    institution = Column(String, nullable=True)


class Client(Base):
    __tablename__ = "client"
    client_num = Column(Integer, nullable=False, primary_key=True)
    client_name = Column(String, nullable=False)


engine = create_engine("sqlite:///{0}".format(SQLITE_DB_PATH))
Base.metadata.create_all(engine)
