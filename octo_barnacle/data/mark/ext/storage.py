from flask import current_app
from pymongo import MongoClient
from octo_barnacle.data.mark.storage import MarkStickerStorage


class _StorageState:

    def __init__(self, storage=None):
        self.storage = storage


class StickerStorageExt:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('MARK_MONGO_HOST', '127.0.0.1')
        app.config.setdefault('MARK_MONGO_PORT', 27017)
        app.config.setdefault('MARK_MONGO_DB', 'octo_barnacle')
        app.extensions['mark_storage'] = _StorageState()

    @property
    def storage(self):
        state = current_app.extensions['mark_storage']
        if state.storage is None:
            db = MongoClient(
                current_app.config['MARK_MONGO_HOST'],
                current_app.config['MARK_MONGO_PORT'],
            )[current_app.config['MARK_MONGO_DB']]
            state.storage = MarkStickerStorage(db)
        return state.storage
