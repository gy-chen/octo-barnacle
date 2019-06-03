from flask import current_app
from telegram import Bot


class TelegramBotExt:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('MARK_BOT_TOKEN', None)

    @property
    def bot(self):
        return Bot(current_app.config['MARK_BOT_TOKEN'])
