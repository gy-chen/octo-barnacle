import os
import bson
import pytest
import tensorflow as tf
from pymongo import MongoClient
from octo_barnacle.train import dataset
from octo_barnacle.train.emoji import predefined
from octo_barnacle import storage
from octo_barnacle.config import MongoConfig

basepath = os.path.dirname(__file__)


@pytest.fixture
def db():
    client = MongoClient(MongoConfig.HOST, MongoConfig.PORT)
    db = client.test_database
    yield db
    client.drop_database('test_database')


@pytest.fixture
def sample_stickers():
    with open(os.path.join(basepath, 'sample_stickers.bson'), 'rb') as f:
        content = f.read()
    return bson.BSON.decode(content)['stickers']


@pytest.fixture
def sample_stickerset():
    with open(os.path.join(basepath, 'sample_stickerset.bson'), 'rb') as f:
        content = f.read()
    return bson.BSON.decode(content)


@pytest.fixture
def storage_(db, sample_stickerset, sample_stickers):
    storage_ = storage.StickerStorage(db)
    storage_.store(sample_stickerset, sample_stickers)
    return storage_


@pytest.fixture(scope='module')
def test_tfrecords_filename():
    filename = 'test.tfrecrod'
    yield filename
    os.remove(filename)


def test_save_to_tfrecords(storage_, test_tfrecords_filename):
    with tf.Session() as sess:
        ds = dataset.get_tf_dataset(storage_)
        sess.run(dataset.save_tf_dataset(ds, test_tfrecords_filename))


def test_load_tfrecords(test_tfrecords_filename):
    with tf.Session() as sess:
        ds = dataset.load_tf_dataset(test_tfrecords_filename)
        ds_iter = ds.make_initializable_iterator()
        sess.run(ds_iter.initializer)
        el = sess.run(ds_iter.get_next())
        assert el[0].shape == (dataset.IMAGE_SIZE,
                               dataset.IMAGE_SIZE, 3)
        assert el[1].shape == (len(predefined.emojis), )
