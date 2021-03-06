from flask import current_app
from redis import Redis
from octo_barnacle.data.mark.lockmanager import MarkStickersetLockManager


class MarkStickersetLockManagerExt:

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('MARK_REDIS_HOST', '127.0.0.1')
        app.config.setdefault('MARK_REDIS_PORT', 6379)

    @property
    def lockmanager(self):
        return MarkStickersetLockManager(Redis(
            current_app.config['MARK_REDIS_HOST'],
            current_app.config['MARK_REDIS_PORT']
        ))
