import logbook

from sqlalchemy import update

from src.db.db import *
from src.data import correct_names


def get_dpoh_name_freq():
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


def fix_mispelled_dpoh_names():

    logbook.debug("computing correct names")
    names = get_dpoh_name_freq()
    df = correct_names.find_correct_names(names)

    conn = get_sqlalchemy_connection()
    trans = conn.begin()

    counter = 0
    logbook.debug("updating db")
    for row in df.iterrows():
        row = row[1]

        firstname = row["firstname"]
        lastname = row["lastname"]
        correct_firstname = row["correct_firstname"]
        correct_lastname = row["correct_lastname"]

        stmt = update(CommunicationDPOH.__table__).where(
            CommunicationDPOH.dpoh_first_name == firstname
        ).where(
            CommunicationDPOH.dpoh_last_name == lastname
        ).values(
            dpoh_first_name=correct_firstname,
            dpoh_last_name=correct_lastname
        )
        trans.connection.execute(stmt)

        counter += 1
        if counter % 100 == 0:
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


