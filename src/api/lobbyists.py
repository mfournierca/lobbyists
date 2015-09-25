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


def publicservant_itinerary(lastname=None, firstname=None, limit=100):
    """Get the itinerary of lobbyist meetings for a given public servant."""
    lastname = clean_name(lastname) if lastname else ""
    firstname = clean_name(firstname) if firstname else ""

    import pdb
    pdb.set_trace()

    query = SESSION.query(db.DPOHCommDetailsView)
    query = query.filter_by(dpoh_last_name=lastname)
    query = query.filter_by(dpoh_first_name=firstname)
    query = query.order_by(db.DPOHCommDetailsView.com_date)
    query = query.limit(limit)
    results = query.all()

    response = {
        "message": None,
        "data": {
            "dpoh_last_name": lastname,
            "dpoh_first_name": firstname,
            "limit": limit,
            "count": len(results),
            "itinerary": defaultdict(list)
        }
    }
    for r in results:
        response["data"]["itinerary"][r.com_date_str()].append({
            "reg_first_name": r.registrant_first_name,
            "reg_last_name": r.registrant_last_name,
            "comlog_id": r.comlog_id,
            "subject_matter": r.subject_matter,
            "client_name": r.client_name
        })
    return response


@APP.route(BASE_PATH.format("publicservant/<lastname>_<firstname>/itinerary"))
def _publicservant_itinerary(lastname=None, firstname=None):
    limit = request.args.get("limit", 100)
    limit = int(limit)

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

