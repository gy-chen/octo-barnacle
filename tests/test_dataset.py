import os
import bson
import pytest
import tensorflow as tf
import numpy as np
from pymongo import MongoClient
from PIL import Image
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


def test_resize_small_image():
    small_fat_image = Image.new('RGB', (100, 60), (255, 255, 255))
    resized_small_fat_image = np.asarray(
        dataset._resize_sticker_image(small_fat_image, 128))
    assert resized_small_fat_image.shape == (128, 128, 3)
    assert np.all(resized_small_fat_image[:76, :, :] == 255)
    assert np.all(resized_small_fat_image[76:, :, :] == 0)

    small_tall_image = Image.new('RGB', (60, 100), (255, 255, 255))
    resized_small_tall_image = np.asarray(
        dataset._resize_sticker_image(small_tall_image, 128)
    )
    assert resized_small_tall_image.shape == (128, 128, 3)
    assert np.all(resized_small_tall_image[:, :76, :] == 255)
    assert np.all(resized_small_tall_image[:, 76:, :] == 0)


def test_resize_big_image():
    big_fat_image = Image.new('RGB', (500, 400), (255, 255, 255))
    resized_big_fat_image = np.asarray(
        dataset._resize_sticker_image(big_fat_image, 128)
    )
    assert resized_big_fat_image.shape == (128, 128, 3)
    assert np.all(resized_big_fat_image[:102, :, :] == 255)
    assert np.all(resized_big_fat_image[102:, :, :] == 0)

    big_tall_image = Image.new('RGB', (400, 500), (255, 255, 255))
    resized_big_tall_image = np.asarray(
        dataset._resize_sticker_image(big_tall_image, 128)
    )
    assert resized_big_tall_image.shape == (128, 128, 3)
    assert np.all(resized_big_tall_image[:, :102, :] == 255)
    assert np.all(resized_big_tall_image[:, 102:, :] == 0)
