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
from src import db
from json import dumps
from copy import copy
from collections import defaultdict

from src.common import clean_name

APP = Flask(__name__)
CORS(APP)

SESSION = db.make_sqlalchemy_session()
BASE_PATH = "/api/v1/{0}"
PORT = 5001


@APP.route(BASE_PATH.format("publicservant/<lastname>_<firstname>/itinerary"))
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

    data = dumps(data)
    return Response(data, status=200, mimetype="application/json")


@APP.route(BASE_PATH.format("publicservant/names")
def publicservant_names():
    query = SESSION.query(db.CommunicationDPOH)
    query = query.filter()


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--debug"]:
        APP.debug = True
    APP.run(port=PORT)

