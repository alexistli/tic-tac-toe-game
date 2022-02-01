"""Flask app configuration classes."""
import os
from pathlib import Path
from tempfile import mkdtemp

from dotenv import load_dotenv


basedir = Path(__file__).resolve().parent
load_dotenv(Path(basedir).joinpath("../.env.prod"))


class Config:
    """Base config, uses local staging database."""

    # General Config
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_ENV = os.environ.get("FLASK_ENV")

    # Flask-Session
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_HTTPONLY = False

    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/static/dist"
