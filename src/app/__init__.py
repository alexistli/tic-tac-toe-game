"""Application factory."""
import logging

from config import Config
from flask import Flask
from flask_session import Session


def create_app(config_class=Config):
    """Creates the core application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    Session(app)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:

        app.logger.setLevel(logging.INFO)
        app.logger.info("Game startup")

    return app
