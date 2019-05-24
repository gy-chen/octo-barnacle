import os
from pymongo import MongoClient
from octo_barnacle import storage


def ch_workdir(workdir):
    os.makedirs(workdir, exist_ok=True)
    os.chdir(workdir)


def get_storage(host, port, db):
    db = MongoClient(host, port)[db]
    return storage.StickerStorage(db)
