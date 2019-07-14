import os
import bson
import pytest
import dotenv
from redis import Redis
from pymongo import MongoClient
from octo_barnacle.bot import get_bot
from octo_barnacle.config import MongoConfig

dotenv.load_dotenv()
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
def bot():
    return get_bot()


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


@pytest.fixture
def sample_webp():
    with open(os.path.join(basepath, 'sample_image.webp'), 'rb') as f:
        return f.read()


@pytest.fixture
def app_config():
    class RedisConfig:
        HOST = os.getenv('TEST_REDIS_HOST')
        PORT = int(os.getenv('TEST_REDIS_PORT'))

    class MongoConfig:
        HOST = os.getenv('TEST_MONGO_HOST')
        PORT = int(os.getenv('TEST_MONGO_PORT'))
        DB = os.getenv('TEST_MONGO_DB')

    class WebConfig:
        MARK_BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
        MARK_REDIS_HOST = RedisConfig.HOST
        MARK_REDIS_PORT = RedisConfig.PORT
        MARK_MONGO_HOST = MongoConfig.HOST
        MARK_MONGO_PORT = MongoConfig.PORT
        MARK_MONGO_DB = MongoConfig.DB

    return WebConfig
