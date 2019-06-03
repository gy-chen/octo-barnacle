import os
import bson
import pytest
import dotenv
from redis import Redis
from octo_barnacle.config import MongoConfig
from pymongo import MongoClient

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
