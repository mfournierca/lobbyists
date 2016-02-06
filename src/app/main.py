"""The lobbyists webapp.

Usage:
    main.py [options]

Options:
    --help   Show this help page
    --debug  Enable flask debugging
"""
import logbook
from docopt import docopt
from flask import Flask, render_template, request

from src.data.clean import clean_name

APP = Flask(__name__)

BASE_PATH = "/app/v1/{0}"
PORT = 8081

@APP.route(BASE_PATH.format("itinerary"))
def itinerary():
    """The itinerary app page."""
    dpoh_firstname = clean_name(request.args.get("firstname", "Stephen"))
    dpoh_lastname = clean_name(request.args.get("lastname", "Harper"))

    return render_template("itinerary.html.j2", dpoh_firstname=dpoh_firstname, dpoh_lastname=dpoh_lastname)

if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--debug"]:
        APP.debug = True
    APP.run(port=PORT)
