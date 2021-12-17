"""Application factory."""
from config import Config
from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO

session = Session()
socketio = SocketIO(logger=True, engineio_logger=False)


def create_app(config_class=Config):
    """Creates the core application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    session.init_app(app)
    socketio.init_app(app, async_mode=None)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
