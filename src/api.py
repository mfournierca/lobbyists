"""The API for the lobbyists application.

Usage:
    api.py [options]

Options:
    --help   Show this help page
    --debug  Activate Flask debugging.
"""

from docopt import docopt
from flask import Flask
from src import db

app = Flask(__name__)
conn = db.make_connection()


@app.route("/publicservant/<lastname>_<firstname>/itinerary")
def itinerary(lastname=None, firstname=None):
    """Get the itinerary of lobbyist meetings for a given public servant."""
    return "{0}, {1}".format(lastname, firstname)


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--debug"]:
        app.debug = True
    app.run()

