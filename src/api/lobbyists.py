"""The API for the lobbyists application.

Usage:
    api.py [options]

Options:
    --help   Show this help page
    --debug  Activate Flask debugging.
"""
import logbook

from docopt import docopt
from flask import Flask, Response
from flask.ext.cors import CORS
from src.db import db
from json import dumps
from sqlalchemy import asc, desc, func, text
from collections import defaultdict

from src.data.clean import clean_name

APP = Flask(__name__)
CORS(APP)

SESSION = db.make_sqlalchemy_session()
BASE_PATH = "/api/v1/{0}"
PORT = 5001


def client_frequency(lastname=None, firstname=None, limit=100):
    """Rank the clients (i.e. lobbyists) by the number of times they met with
    the specified public servant"""
    lastname = clean_name(lastname) if lastname else ""
    firstname = clean_name(firstname) if firstname else ""

    expression = text("""
    SELECT comlog_id, client_name, com_date, COUNT(client_name) as count_client_name
    FROM (
        SELECT DISTINCT comlog_id, client_name, com_date
        FROM dpoh_com_details
        WHERE dpoh_last_name == :lastname
            AND dpoh_first_name == :firstname
    )
    GROUP BY client_name
    ORDER BY count_client_name DESC
    LIMIT :limit
    """).bindparams(lastname=lastname, firstname=firstname, limit=limit)
    query = SESSION.execute(expression)
    return query.fetchall()


def publicservant_itinerary(lastname=None, firstname=None, limit=100):
    """Get the itinerary of lobbyist meetings for a given public servant."""
    lastname = clean_name(lastname) if lastname else ""
    firstname = clean_name(firstname) if firstname else ""

    query = SESSION.query(db.DPOHCommDetailsView)
    query = query.filter(db.DPOHCommDetailsView.dpoh_last_name == lastname)
    query = query.filter(db.DPOHCommDetailsView.dpoh_first_name == firstname)
    query.order_by(db.DPOHCommDetailsView.com_date)
    query.limit(limit)

    data = {
        "dpoh_last_name": lastname,
        "dpoh_first_name": firstname,
        "itinerary": defaultdict(list)
    }
    for r in query.all():
        data["itinerary"][r.com_date_str()].append({
            "reg_first_name": r.registrant_first_name,
            "reg_last_name": r.registrant_last_name,
            "comlog_id": r.comlog_id,
            "subject_matter": r.subject_matter,
            "client_name": r.client_name
        })
    return data


@APP.route(BASE_PATH.format("publicservant/<lastname>_<firstname>/itinerary"))
def _publicservant_itinerary(lastname=None, firstname=None, limit=100):
    data = publicservant_itinerary(
        lastname=lastname,
        firstname=firstname,
        limit=limit
    )
    data = dumps(data)
    return Response(data, status=200, mimetype="application/json")


def publicservant_names(limit=1000):
    query = SESSION.query(
        db.CommunicationDPOH.dpoh_last_name,
        db.CommunicationDPOH.dpoh_first_name)
    query = query.distinct()
    query = query.order_by(asc(db.CommunicationDPOH.dpoh_last_name))
    query.limit(limit)
    return [(r.dpoh_last_name, r.dpoh_first_name) for r in query.all()]


@APP.route(BASE_PATH.format("publicservant/names"))
def _publicservant_names(limit=1000):
    data = publicservant_names(limit=limit)
    data = dumps(data)
    return Response(data, status=200, mimetype="application/json")


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--debug"]:
        APP.debug = True
    APP.run(port=PORT)

