from flask import current_app
from octo_barnacle.data.mark.model import MarkModel


class _ModelExtState:
    def __init__(self, storage_ext, lockmanager_ext):
        self.storage_ext = storage_ext
        self.lockmanager_ext = lockmanager_ext
        self.model = None


class ModelExt:

    def __init__(self, app=None, storage=None, lockmanager=None):
        if app is not None:
            self.init_app(app, storage, lockmanager)

    def init_app(self, app, storage, lockmanager):
        app.extensions['mark_model'] = _ModelExtState(storage, lockmanager)

    @property
    def model(self):
        state = current_app.extensions['mark_model']
        if state.model is None:
            state.model = MarkModel(state.storage_ext.storage, state.lockmanager_ext.lockmanager)
        return state.model
