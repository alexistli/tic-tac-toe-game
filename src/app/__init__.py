"""Application factory."""
from typing import Type

import eventlet

eventlet.monkey_patch()

import structlog  # noqa: E402
from config import Config  # noqa: E402
from flask import Flask  # noqa: E402
from flask_assets import Bundle  # noqa: E402
from flask_assets import Environment  # noqa: E402
from flask_session import Session  # noqa: E402
from flask_socketio import SocketIO  # noqa: E402


ASYNC_MODE = "eventlet"

session = Session()
socketio = SocketIO()
assets = Environment()

logger = structlog.get_logger()  # logger configured in logging_setup.py


def create_app(config_class: Type[Config] = Config) -> Flask:
    """Creates and configure an instance of the Flask application."""
    app: Flask = Flask(__name__)
    app.config.from_object(config_class)

    session.init_app(app)
    socketio.init_app(app, async_mode=ASYNC_MODE, manage_session=False, logger=logger)

    assets.init_app(app)
    with app.app_context():
        _compile_static_assets(assets)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app


def _compile_static_assets(assets_):
    """Configures and builds asset bundles."""
    css = Bundle("src/main.css", output="dist/main.css", filters="postcss")
    js = Bundle("src/*.js", output="dist/main.js")

    assets.register("css", css)
    assets.register("js", js)

    css.build()
    js.build()
