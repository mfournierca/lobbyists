from os.path import join
from src.constants import DATA_ROOT

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

SQLITE_DB_PATH = join(DATA_ROOT, "sqlite.db")

Base = declarative_base()


class SubjectMatter(Base):
    __tablename__ = "subject_matter"
    comlog_id = Column(Integer, primary_key=True)
    subject_matter = Column(String, nullable=False)
    other_subject_matter = Column(String, nullable=True)


engine = create_engine("sqlite:///{0}".format(SQLITE_DB_PATH))
Base.metadata.create_all(engine)
