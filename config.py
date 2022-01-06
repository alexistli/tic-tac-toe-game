"""Flask app configuration classes."""
import os
from pathlib import Path
from tempfile import mkdtemp

from dotenv import load_dotenv


basedir = Path(__file__).resolve().parent
load_dotenv(Path(basedir).joinpath(".env"))


class Config:
    """Base config, uses local staging database."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
