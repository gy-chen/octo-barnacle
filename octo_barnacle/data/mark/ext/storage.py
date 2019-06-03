from octo_barnacle.data.mark.storage import MarkStickerStorage
from pymongo import MongoClient


class _StorageState:

    def __init__(self, storage=None):
        self.storage = storage


class StickerStorageExt:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.set_default('MARK_MONGO_HOST', '127.0.0.1')
        app.config.set_defualt('MARK_MONGO_PORT', 27017)
        app.config.set_default('MARK_MONGO_DB', 'octo_barnacle')
        app.extensions['mark_storage'] = _StorageState()

    @property
    def storage(self):
        state = app.extensions['mark_storage']
        if state.storage is None:
            db = MongoClient(
                app.config['MARK_MONGO_HOST'],
                app.config['MARK_MONGO_PORT'],
            )[app.config['MARK_MONGO_DB']]
            state.storage = MarkStickerStorage(db)
        return state.storage
