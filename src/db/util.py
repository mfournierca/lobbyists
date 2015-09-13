from src.db.db import *


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


def fix_mispelled_dpoh_names():
    pass
