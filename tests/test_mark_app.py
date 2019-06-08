import os
import pytest
import dotenv
from redis import Redis
from pymongo import MongoClient
from octo_barnacle.data.mark import create_app
from octo_barnacle.data.mark import ext

dotenv.load_dotenv()


@pytest.fixture
def mark_app_config():
    class RedisConfig:
        HOST = os.getenv('TEST_REDIS_HOST')
        PORT = int(os.getenv('TEST_REDIS_PORT'))

    class MongoConfig:
        HOST = os.getenv('TEST_MONGO_HOST')
        PORT = int(os.getenv('TEST_MONGO_PORT'))
        DB = os.getenv('TEST_MONGO_DB')

    class WebConfig:
        BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
        REDIS = RedisConfig
        MONGO = MongoConfig

    return WebConfig


@pytest.fixture
def app(mark_app_config, sample_stickerset, sample_stickers):
    app = create_app(mark_app_config)
    app.config['TESTING'] = True

    with app.app_context():
        ext.storage.storage.store(sample_stickerset, sample_stickers)

    yield app

    r = Redis(
        host=mark_app_config.REDIS.HOST,
        port=mark_app_config.REDIS.PORT
    )
    r.flushall()

    mongo = MongoClient(
        mark_app_config.MONGO.HOST,
        mark_app_config.MONGO.PORT,
    )
    mongo.drop_database(mark_app_config.MONGO.DB)


@pytest.fixture
def client(app):
    return app.test_client()


def test_next_batch(client):
    batch = client.post('/stickerset/mark/next_batch')

    item = batch.get_json()
    assert batch.status_code == 200
    assert len(item['batch']) == 1
    assert type(item['batch'][0]['resource']) is str
    assert len(item['batch'][0]['stickers']) == 7
    assert item['batch'][0]['stickerset']['name'] == 'ChuunibyoudemoKoigaShitai'
    assert item['batch'][0]['stickerset']['title'] == 'Chuunibyou demo Koi ga Shitai'

    empty_batch = client.post('/stickerset/mark/next_batch')
    empty_item = empty_batch.get_json()
    assert empty_batch.status_code == 200
    assert len(empty_item['batch']) == 0


def test_mark(client):
    batch = client.post('/stickerset/mark/next_batch')
    batch_item = batch.get_json()

    stickerset_name = batch_item['batch'][0]['stickerset']['name']
    resource = batch_item['batch'][0]['resource']

    mark = client.post(f'/stickerset/{stickerset_name}/mark', data={
        'resource': resource,
        'mark': 'OTHER'
    })

    assert mark.status_code == 200
