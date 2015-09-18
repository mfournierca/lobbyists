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

