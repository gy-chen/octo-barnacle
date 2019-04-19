"""Store shared variables."""
import pymongo
from octo_barnacle.storage import StickerStorage
from octo_barnacle.config import MongoConfig
from octo_barnacle.config import RedisConfig

storage = None
lock_manager = None


def get_storage(config=MongoConfig):
    global storage
    if storage is None:
        client = pymongo.MongoClient(config.HOST, config.PORT)
        db = client[config.DB]
        storage_ = StickerStorage(db)
        storage = storage_
    return storage


def get_lock_manager(config=RedisConfig):
    global lock_manager
    if lock_manager is None:
        r = redis.Redis(RedisConfig.HOST, RedisConfig.PORT)
        lock_manager = LockManager(r)
    return lock_manager
