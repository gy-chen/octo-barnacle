import hashlib
import time
import os
import pytest
from redis import Redis
from pymongo import MongoClient
from octo_barnacle.bot import get_bot
from octo_barnacle.bot import context
from octo_barnacle.storage import StickerStorage
from octo_barnacle.config import MongoConfig
from octo_barnacle import model
from octo_barnacle import lock


@pytest.fixture
def bot():
    return get_bot()


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
    lm = lock.LockManager(redis, 10)
    context.lock_manager = lm
    return lm


@pytest.fixture
def db():
    client = MongoClient()
    yield client.test_database
    client.drop_database('test_database')


@pytest.fixture
def storage(db):
    s = StickerStorage(db)
    context.storage = s
    return s


def test_get_stickerset(bot):
    stickerset = model._get_stickerset(bot, 'python')
    assert stickerset['name'] == 'Python'
    assert stickerset['title'] == 'Python'


def test_get_stickers(bot):
    stickers = list(model._get_stickers(bot, 'python'))
    assert len(stickers) == 1
    sticker = stickers[0]
    assert sticker['image_id'] == 'CAADBQADCAIAAv-EDwMwropGUQmLWQI'
    assert sticker['stickerset_name'] == 'Python'
    assert sticker['emoji'] == '🐍'
    assert hashlib.md5(sticker['image']).hexdigest(
    ) == '2c5feb400b16bf73c47a68bfd4512181'
    assert sticker['image_path'].startswith(
        'https://api.telegram.org/file/bot')
    assert sticker['image_path'].endswith('.webp')
    assert sticker['image_width'] == 512
    assert sticker['image_height'] == 512


def test_lock(bot, storage, lock_manager):
    model.collect_stickerset(bot, storage, lock_manager, 'Python')

    with pytest.raises(lock.LockError):
        model.collect_stickerset(bot, storage, lock_manager, 'Python')

    time.sleep(11)
    model.collect_stickerset(bot, storage, lock_manager, 'Python')


def test_not_exists_stickerset(bot, storage, lock_manager, redis):
    not_exists_stickerset = 'AAABBBCC NOT EXISTS STICKERSET AAABBBCCC'
    with pytest.raises(model.StickerSetNotFoundError):
        model.collect_stickerset(
            bot, storage, lock_manager, not_exists_stickerset)

    assert redis.get(not_exists_stickerset) is not None


def test_empty_stickers(bot, storage, lock_manager):
    model.collect_stickerset(bot, storage, lock_manager, 'Naruto')
