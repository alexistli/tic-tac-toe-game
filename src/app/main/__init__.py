"""Main Application Blueprint."""
from flask import Blueprint


bp = Blueprint("main", __name__)

from app.main import events  # noqa: E402, F401 (remove F401 later)
from app.main import routes  # noqa: E402, F401 (remove F401 later)
