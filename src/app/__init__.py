"""Application factory."""
import logging
from typing import Type

from config import Config
from flask import Flask
from flask_assets import Bundle
from flask_assets import Environment
from flask_session import Session
from flask_socketio import SocketIO


ASYNC_MODE = "eventlet"

session = Session()
socketio = SocketIO()

logger = logging.getLogger("app")  # logger configured in gunicorn.conf.py


def create_app(config_class: Type[Config] = Config) -> Flask:
    """Creates the core application."""
    app: Flask = Flask(__name__)
    app.config.from_object(config_class)

    # attach the logger and its handlers to the Flask app
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
    logger.info("Flask game")

    session.init_app(app)
    socketio.init_app(app, async_mode=ASYNC_MODE, manage_session=False, logger=logger)

    assets = Environment(app)
    css = Bundle("src/main.css", output="dist/main.css", filters="postcss")
    js = Bundle("src/*.js", output="dist/main.js")
    assets.register("css", css)
    assets.register("js", js)
    css.build()
    js.build()

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
