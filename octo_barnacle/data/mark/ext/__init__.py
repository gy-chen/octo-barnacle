"""Flask extensions for mark stickerset web interface

"""
from .bot import TelegramBotExt
from .lockmanager import MarkStickersetLockManagerExt
from .storage import StickerStorageExt

bot = TelegramBotExt()
lockmanager = MarkStickersetLockManagerExt()
storage = StickerStorageExt()
