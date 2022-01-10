"""Application factory."""
import logging
from typing import Type

from config import Config
from flask import Flask
from flask_assets import Bundle
from flask_assets import Environment
from flask_session import Session
from flask_socketio import SocketIO


FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")


async_mode = "eventlet"

session = Session()
socketio = SocketIO()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(FORMATTER)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


def create_app(config_class: Type[Config] = Config) -> Flask:
    """Creates the core application."""
    app: Flask = Flask(__name__)
    app.config.from_object(config_class)

    app.logger = logger
    app.logger.info("Flask game")

    session.init_app(app)
    socketio.init_app(
        app, async_mode=async_mode, manage_session=False, logger=app.logger
    )

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
