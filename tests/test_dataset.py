import pytest
from pymongo import MongoClient
from octo_barnacle.train import dataset
from octo_barnacle import storage
from octo_barnacle.config import MongoConfig


@pytest.fixture(scope='function')
def db():
    client = MongoClient(MongoConfig.HOST, MongoConfig.PORT)
    # TODO change me later
    yield client['octo_barnacle']


@pytest.fixture
def storage_(db):
    return storage.StickerStorage(db)


def test_gen_sticker_records(storage_):
    records = dataset._gen_sticker_records(storage_)
    records = list(records)
    breakpoint()
