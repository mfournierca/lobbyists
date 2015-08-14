"""The API for the lobbyists application.

Usage:
    api.py [options]

Options:
    --help   Show this help page
    --debug  Activate Flask debugging.
"""
import logbook

from docopt import docopt
from flask import Flask
from src import db

from src.common import clean_name

APP = Flask(__name__)
CONN = db.make_session()


@APP.route("/publicservant/<lastname>_<firstname>/itinerary")
def itinerary(lastname=None, firstname=None):
    """Get the itinerary of lobbyist meetings for a given public servant."""
    lastname = clean_name(lastname) if lastname else ""
    firstname = clean_name(firstname) if firstname else ""
    cur = CONN.cursor()

    return "{0}, {1}".format(lastname, firstname)


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--debug"]:
        APP.debug = True
    APP.run()

