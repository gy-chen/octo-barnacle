from pymongo import MongoClient
from octo_barnacle import storage


def get_storage(host, port, db):
    db = MongoClient(host, port)[db]
    return storage.StickerStorage(db)
