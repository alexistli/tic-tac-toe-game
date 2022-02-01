"""Flask app configuration classes."""
import os
from tempfile import mkdtemp


class Config:
    """Base config, uses local staging database."""

    # General Config
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # Flask-Session
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_HTTPONLY = False

    STATIC_FOLDER = f"{os.environ.get('APP_FOLDER')}/static/dist"
