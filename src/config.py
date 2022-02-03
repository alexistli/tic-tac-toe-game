"""Flask app configuration classes."""
import os
from tempfile import mkdtemp


class Config:
    """Base config."""

    # General Config
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    STATIC_FOLDER = f"{os.environ.get('APP_FOLDER')}/static/dist"

    # Flask-Session
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_HTTPONLY = False
