"""Flask app routes."""
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

from app.main import bp


@bp.route("/")
def index():
    """Shows the current game."""
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    return render_template("game.html", game=session["board"], turn=session["turn"])


@bp.route("/play/<int:row>/<int:col>")
def play(row, col):
    """Gets the coordinates of the played cell."""
    return redirect(url_for("main.index"))
