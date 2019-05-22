"""provide function for processing image to emoji dataset
"""
import functools
import io
import logging
import numpy as np
import tensorflow as tf
from PIL import Image
from sklearn import preprocessing
from .emoji import predefined
from .utils import get_storage

logger = logging.getLogger(__name__)

TRAIN_IMAGE_SIZE = 128
TRAIN_IMAGE_DROP_SIZE = 102
IMAGE_DEPTH = 255


def get_tf_dataset():
    # TODO
    storage = get_storage('127.0.0.1', 27017, 'octo_barnacle')
    ds = tf.data.Dataset.from_generator(
        functools.partial(_gen_sticker_records, storage),
        (tf.float32, tf.float32),
        (tf.TensorShape([128, 128, 3]), tf.TensorShape([3836]))
    )
    return ds


def _gen_sticker_records(storage):
    """prcocess and generate stored stickers

    this method does:
        - interpret webp image content
        - resize image to fixed size

    Arguments:
        storage (octo_barnacle.storage.StickerStorage)

    Returns:
        iterable that generate ((img_w, img_h, img_channel), emoji)
    """
    for sticker in storage.get_stickers():
        try:
            yield _sticker_to_record(sticker)
        except _DropImageException:
            continue


def _sticker_to_record(sticker):
    img = _sticker_image_to_array(sticker['image'])
    # drop alpha
    img = img[:, :, :3]
    img = (img - IMAGE_DEPTH / 2) / IMAGE_DEPTH
    label_binarizer = _get_label_binarizer()
    label = label_binarizer.transform([sticker['emoji']])
    label = label.reshape(-1)
    return (img, label)


def _sticker_image_to_array(image_content):
    buf = io.BytesIO(image_content)
    img = Image.open(buf)
    if img.width < TRAIN_IMAGE_DROP_SIZE or img.height < TRAIN_IMAGE_DROP_SIZE:
        logger.info('drop small size image {}x{}'.format(
            img.width, img.height))
        raise _DropImageException()
    img = img.resize((TRAIN_IMAGE_SIZE, TRAIN_IMAGE_SIZE))
    return np.asarray(img)


class _DropImageException(Exception):
    pass


label_binarizer = None


def _get_label_binarizer():
    global label_binarizer
    if label_binarizer is None:
        label_binarizer = preprocessing.LabelBinarizer()
        label_binarizer.fit(predefined.emojis)
    return label_binarizer
