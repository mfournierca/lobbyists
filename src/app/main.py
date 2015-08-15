"""The lobbyists webapp.

Usage:
    main.py [options]

Options:
    --help   Show this help page
    --debug  Enable flask debugging
"""
import logbook
from docopt import docopt
from flask import Flask, render_template

APP = Flask(__name__)
BASE_PATH = "/app/v1/{0}"
PORT = 8081


@APP.route(BASE_PATH.format("itinerary"))
def itinerary():
    """Home page of the web app.

    The view and controller are managed by javascript and d3. The model is the
    api.
    """
    return render_template("itinerary.html.j2")


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--debug"]:
        APP.debug = True
    APP.run(port=PORT)
