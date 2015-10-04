"""The API for the lobbyists application.

Usage:
    api.py [options]

Options:
    --help   Show this help page
    --debug  Activate Flask debugging.
"""
import logbook

from docopt import docopt
from flask import Flask, Response, request
from flask.ext.cors import CORS
from src.db import db, util
from json import dumps
from sqlalchemy import asc
from collections import defaultdict

from src.data.clean import clean_name

APP = Flask(__name__)
CORS(APP)

SESSION = util.make_sqlalchemy_session()
BASE_PATH = "/api/v1/{0}"
PORT = 5001


def publicservant_itinerary(lastname=None, firstname=None):
    """Get the itinerary of lobbyist meetings for a given public servant."""
    lastname = clean_name(lastname) if lastname else ""
    firstname = clean_name(firstname) if firstname else ""

    query = SESSION.query(db.DPOHCommDetailsView)
    query = query.filter_by(dpoh_last_name=lastname)
    query = query.filter_by(dpoh_first_name=firstname)
    query = query.order_by(db.DPOHCommDetailsView.com_date)
    results = query.all()

    response = {
        "message": None,
        "data": {
            "dpoh_last_name": lastname,
            "dpoh_first_name": firstname,
            "count": len(results),
            "itinerary": []
        }
    }
    for r in results:
        response["data"]["itinerary"].append({
            "date": r.com_date_str(),
            "reg_first_name": r.registrant_first_name,
            "reg_last_name": r.registrant_last_name,
            "comlog_id": r.comlog_id,
            "subject_matter": r.subject_matter,
            "client_name": r.client_name
        })
    return response


@APP.route(BASE_PATH.format("publicservant/<lastname>_<firstname>/itinerary"))
def _publicservant_itinerary(lastname=None, firstname=None):
    data = publicservant_itinerary(
        lastname=lastname,
        firstname=firstname
    )
    data = dumps(data)
    return Response(data, status=200, mimetype="application/json")


def publicservant_names():
    query = SESSION.query(
        db.CommunicationDPOH.dpoh_last_name,
        db.CommunicationDPOH.dpoh_first_name)
    query = query.distinct()
    query = query.order_by(asc(db.CommunicationDPOH.dpoh_last_name))
    return [(r.dpoh_last_name, r.dpoh_first_name) for r in query.all()]


@APP.route(BASE_PATH.format("publicservant/names"))
def _publicservant_names():
    data = publicservant_names()
    data = dumps(data)
    return Response(data, status=200, mimetype="application/json")


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--debug"]:
        APP.debug = True
    APP.run(port=PORT)

