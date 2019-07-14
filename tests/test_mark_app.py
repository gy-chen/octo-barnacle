import os
import pytest
import dotenv
from redis import Redis
from pymongo import MongoClient
from octo_barnacle.data.mark import create_app
from octo_barnacle.data.mark import ext

dotenv.load_dotenv()


@pytest.fixture
def app(app_config, sample_stickerset, sample_stickers):
    app = create_app(app_config)
    app.config['TESTING'] = True

    with app.app_context():
        ext.storage.storage.store(sample_stickerset, sample_stickers)

    yield app

    r = Redis(
        host=app_config.MARK_REDIS_HOST,
        port=app_config.MARK_REDIS_PORT
    )
    r.flushall()

    mongo = MongoClient(
        app_config.MARK_MONGO_HOST,
        app_config.MARK_MONGO_PORT,
    )
    mongo.drop_database(app_config.MARK_MONGO_DB)


@pytest.fixture
def client(app):
    return app.test_client()


def test_next_batch(client):
    batch = client.post('/api/stickerset/mark/next_batch')

    item = batch.get_json()
    assert batch.status_code == 200
    assert len(item['batch']) == 1
    assert type(item['batch'][0]['resource']) is str
    assert len(item['batch'][0]['stickers']) == 7
    assert item['batch'][0]['stickerset']['name'] == 'ChuunibyoudemoKoigaShitai'
    assert item['batch'][0]['stickerset']['title'] == 'Chuunibyou demo Koi ga Shitai'

    empty_batch = client.post('/api/stickerset/mark/next_batch')
    empty_item = empty_batch.get_json()
    assert empty_batch.status_code == 200
    assert len(empty_item['batch']) == 0


def test_mark(client):
    batch = client.post('/api/stickerset/mark/next_batch')
    batch_item = batch.get_json()

    stickerset_name = batch_item['batch'][0]['stickerset']['name']
    resource = batch_item['batch'][0]['resource']

    mark = client.post(f'/api/stickerset/{stickerset_name}/mark', data={
        'resource': resource,
        'mark': 'OTHER'
    })

    assert mark.status_code == 200
