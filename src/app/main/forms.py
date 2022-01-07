"""Forms."""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class CreateMultiGame(FlaskForm):  # type: ignore[misc]
    """TODO."""

    game_name = StringField("Game name", validators=[DataRequired()])
    submit = SubmitField("Create game")


class JoinMultiGame(FlaskForm):  # type: ignore[misc]
    """TODO."""

    game_name = StringField("Game name", validators=[DataRequired()])
    submit = SubmitField("Join game")
