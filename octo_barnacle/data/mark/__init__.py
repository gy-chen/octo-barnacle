"""Web interface for marking stickersets

Some collected stickersets are not suit for training image to emoji classifeier,
this package help to mark these stickersets.
"""
from flask import Flask
from flask_cors import CORS
from .config import WebConfig
from .api import bp as api_bp
from . import ext


def create_app(config=WebConfig):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(config)
    app.config['WTF_CSRF_ENABLED'] = False

    ext.bot.init_app(app)
    ext.lockmanager.init_app(app)
    ext.storage.init_app(app)
    ext.model.init_app(app, ext.storage, ext.lockmanager)

    app.register_blueprint(api_bp)

    return app


app = create_app()
