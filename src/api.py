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
from src import db
from json import dumps
from copy import copy

from src.common import clean_name

APP = Flask(__name__)
SESSION = db.make_sqlalchemy_session()

BASE_RESPONSE = {
    "status": True,
    "message": "",
    "content": None
}


@APP.route("/publicservant/<lastname>_<firstname>/itinerary")
def publicservant_itinerary(lastname=None, firstname=None, limit=100):
    """Get the itinerary of lobbyist meetings for a given public servant."""
    lastname = clean_name(lastname) if lastname else ""
    firstname = clean_name(firstname) if firstname else ""

    query = SESSION.query(db.DPOHCommDetailsView)
    query = query.filter(db.DPOHCommDetailsView.dpoh_last_name == lastname)
    query = query.filter(db.DPOHCommDetailsView.dpoh_first_name == firstname)
    query.order_by(db.DPOHCommDetailsView.com_date)
    query.limit(limit)

    data = copy(BASE_RESPONSE)
    data["content"] = [r.to_dict() for r in query.all()]
    data = dumps(data)

    return Response(data, status=200, mimetype="application/json")


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--debug"]:
        APP.debug = True
    APP.run()

