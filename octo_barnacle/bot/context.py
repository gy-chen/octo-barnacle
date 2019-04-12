"""Store shared variables."""
import pymongo
from octo_barnacle.storage import StickerStorage
from octo_barnacle.config import MongoConfig

storage = None


def get_storage(config=MongoConfig):
    global storage
    if storage is None:
        client = pymongo.MongoClient(config.HOST, config.PORT)
        db = client[config.DB]
        storage_ = StickerStorage(db)
        storage = storage_
    return storage
