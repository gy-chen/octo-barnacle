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
    return bson.decode_all(content)


def test_storage(db, sample_stickerset, sample_stickers):
    sticker_storage = storage.StickerStorage(db)
    sticker_storage.store(sample_stickerset, sample_stickers)

    stickerset = next(sticker_storage.get_stickersets())
    assert stickerset['name'] == sample_stickerset['name']
    assert stickerset['title'] == sample_stickerset['title']

    sticker = next(sticker_storage.get_stickers(stickerset['name']))
    sample_sticker = sample_stickers[0]
    assert sticker['image_id'] == sample_sticker['image_id']
    assert sticker['stickerset_name'] == sample_sticker['stickerset_name']
    assert sticker['emoji'] == sample_sticker['emoji']
    assert sticker['image'] == sample_sticker['image']
    assert sticker['image_path'] == sample_sticker['image_path']
    assert sticker['image_width'] == sample_sticker['image_width']
    assert sticker['image_height'] == sample_sticker['image_height']


def test_insert_empty_stickers(db, sample_stickerset):
    sticker_storage = storage.StickerStorage(db)
    sticker_storage.store(sample_stickerset, [])

    def gen_empty_stickers():
        yield

    sticker_storage.store(sample_stickerset, gen_empty_stickers())
