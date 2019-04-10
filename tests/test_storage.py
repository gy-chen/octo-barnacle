import os
import bson
import pytest
from pymongo import MongoClient
from octo_barnacle import storage
from octo_barnacle.config import MongoConfig

basepath = os.path.dirname(__file__)


@pytest.fixture(scope='function')
def db():
    client = MongoClient(MongoConfig.HOST, MongoConfig.PORT)
    yield client.test_database
    client.drop_database('test_database')


@pytest.fixture
def sample_stickerset():
    with open(os.path.join(basepath, 'sample_stickerset.bson'), 'rb') as f:
        content = f.read()
    return bson.BSON.decode(content)


@pytest.fixture
def sample_stickers():
    with open(os.path.join(basepath, 'sample_stickers.bson'), 'rb') as f:
        content = f.read()
    return bson.BSON.decode(content)['stickers']


def test_storage(db, sample_stickerset, sample_stickers):
    sticker_storage = storage.StickerStorage(db)
    sticker_storage.store(sample_stickerset, sample_stickers)

    stickerset = next(sticker_storage.get_stickersets())
    assert stickerset['name'] == sample_stickerset['name']
    assert stickerset['title'] == sample_stickerset['title']

    sticker = next(sticker_storage.get_stickers(stickerset['name']))
    sample_sticker = sample_stickers[0]
    assert sticker['stickerset_name'] == sample_sticker['stickerset_name']
    assert sticker['emoji'] == sample_sticker['emoji']
    assert sticker['image'] == sample_sticker['image']
    assert sticker['image_path'] == sample_sticker['image_path']
