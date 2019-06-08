"""Flask extensions for mark stickerset web interface

"""
from .bot import TelegramBotExt
from .lockmanager import MarkStickersetLockManagerExt
from .storage import StickerStorageExt
from .model import ModelExt

bot = TelegramBotExt()
lockmanager = MarkStickersetLockManagerExt()
storage = StickerStorageExt()
model = ModelExt()
