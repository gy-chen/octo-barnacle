import time
import os
import bson
import pytest
import pyrogram
from dotenv import load_dotenv
from pymongo import MongoClient
from redis import Redis
from octo_barnacle.storage import StickerStorage
from octo_barnacle.lock import LockManager
from octo_barnacle.bot import context, get_updater
from octo_barnacle.config import MongoConfig

load_dotenv()
basepath = os.path.dirname(__file__)


@pytest.fixture
def redis():
    r = Redis(
        host=os.environ.get('TEST_REDIS_HOST'),
        port=os.environ.get('TEST_REDIS_PORT')
    )
    yield r
    r.flushdb()


@pytest.fixture
def lock_manager(redis):
    lock_manager = LockManager(redis)
    return lock_manager


@pytest.fixture
def db():
    client = MongoClient(MongoConfig.HOST, MongoConfig.PORT)
    yield client.test_database
    client.drop_database('test_database')


@pytest.fixture
def storage(db):
    storage = StickerStorage(db)
    context.storage = storage
    return storage


@pytest.fixture
def updater(storage, lock_manager, monkeypatch):
    monkeypatch.setattr('octo_barnacle.bot.context.storage', storage)
    monkeypatch.setattr('octo_barnacle.bot.context.lock_manager', lock_manager)
    updater = get_updater()
    yield updater
    updater.stop()


@pytest.fixture
def user_client():
    client = pyrogram.Client(
        'octo_barnacle_testing_account',
        api_id=os.environ.get('TEST_PYROGRAM_API_ID'),
        api_hash=os.environ.get('TEST_PYROGRAM_API_HASH')
    )
    with client:
        yield client


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


def test_collect_stickers(updater, storage, user_client, sample_stickerset, sample_stickers):
    updater.start_polling()
    user_client.send_sticker(os.environ.get('TEST_PYROGRAM_BOT_ID'),
                             'CAADBQADCAIAAv-EDwMwropGUQmLWQI')
    time.sleep(10)

    stickerset = next(storage.get_stickersets())
    assert stickerset['name'] == sample_stickerset['name']
    assert stickerset['title'] == sample_stickerset['title']

    sticker = next(storage.get_stickers(stickerset['name']))
    sample_sticker = sample_stickers[0]
    assert sticker['stickerset_name'] == sample_sticker['stickerset_name']
    assert sticker['emoji'] == sample_sticker['emoji']
    assert sticker['image'] == sample_sticker['image']
    assert sticker['image_path'].startswith(
        'http') and sticker['image_path'].endswith('.webp')
    assert sticker['image_width'] == sample_sticker['image_width']
    assert sticker['image_height'] == sample_sticker['image_height']


def test_send_emoji(updater, storage, user_client):
    updater.start_polling()
    user_client.send_sticker(os.environ.get('TEST_PYROGRAM_BOT_ID'),
                             'CAADBQADCAIAAv-EDwMwropGUQmLWQI')
    time.sleep(10)

    user_client.send_message(os.environ.get(
        'TEST_PYROGRAM_BOT_ID'), '\U0001f600')
    user_client.send_message(os.environ.get(
        'TEST_PYROGRAM_BOT_ID'), '\U0001f40d')
    # TODO need a way to check result automatically
    time.sleep(10)
