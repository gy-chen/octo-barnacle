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

logger = logging.getLogger(__name__)

IMAGE_SIZE = 128
IMAGE_DROP_SIZE = 64
IMAGE_DEPTH = 255


def load_tf_dataset(filename):
    """load saved stickers tfrecord file

    Arguments:
        filename (str): path that saved stickers data

    Returns:
        tf.train.Dataset
    """
    raw_dataset = tf.data.TFRecordDataset(filename)
    dataset = raw_dataset.map(_decode_example)
    return dataset


def save_tf_dataset(dataset, filename):
    """save stickers tensorflow dataset into tfrecord file

    Arguments:
        filename (str): path want to save tfrecord file

    Returns:
        tensorflow operation
    """
    serialized_dataset = dataset.map(_tf_serialize_example)
    writer = tf.data.experimental.TFRecordWriter(filename)
    return writer.write(serialized_dataset)


def get_tf_dataset(storage, emojis=predefined.top_10):
    """get stickers tensorflow dataset

    Arguments:
        storage (octo_barnacle.storage.StickerStorage): source of stickers data
        emojis (tuple of str): tuple of accept emoji, will drop sticker if emoji not in this list 

    Returns:
        tf.data.Dataset
    """
    ds = tf.data.Dataset.from_generator(
        functools.partial(_gen_sticker_records, storage, emojis),
        (tf.float32, tf.float32),
        (tf.TensorShape([IMAGE_SIZE, IMAGE_SIZE, 3]),
         tf.TensorShape([len(emojis)]))
    )
    return ds


def _tf_serialize_example(image, label):
    tf_string = tf.py_function(
        _serialize_example,
        (image, label),
        tf.string)
    return tf.reshape(tf_string, ())


def _serialize_example(image, label):
    feature = {
        'image': _bytes_feature(np.array(image).tostring()),
        'label': _bytes_feature(np.array(label).tostring())
    }
    example_proto = tf.train.Example(
        features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()


def _decode_example(serialized_example):
    feature_description = {
        'image': tf.FixedLenFeature([], tf.string),
        'label': tf.FixedLenFeature([], tf.string)
    }
    features = tf.parse_single_example(
        serialized_example,
        features=feature_description
    )

    image = tf.decode_raw(features['image'], tf.float32)
    image = tf.reshape(image, (IMAGE_SIZE, IMAGE_SIZE, 3))

    label = tf.decode_raw(features['label'], tf.float32)

    return image, label


def _gen_sticker_records(storage, emojis):
    """prcocess and generate stored stickers

    this method does:
        - interpret webp image content
        - resize image to fixed size

    Arguments:
        storage (octo_barnacle.storage.StickerStorage)
        emojis (tuple of str): tuple of accept emoji, will drop sticker if emoji not in this list 

    Returns:
        iterable that generate ((img_w, img_h, img_channel), emoji)
    """
    for sticker in storage.get_stickers():
        try:
            yield _sticker_to_record(sticker, emojis)
        except _DropImageException:
            continue
        except _DropUnrecognizedEmojiException:
            continue


def _sticker_to_record(sticker, emojis):
    if sticker['emoji'] not in emojis:
        logger.info(
            'Drop sticker of unrecognized emoji {}'.format(sticker['emoji']))
        raise _DropUnrecognizedEmojiException()
    img = _sticker_image_to_array(sticker['image'])
    # drop alpha
    img = img[:, :, :3]
    img = (img - IMAGE_DEPTH / 2) / IMAGE_DEPTH
    label_binarizer = _get_label_binarizer(emojis)
    label = label_binarizer.transform([sticker['emoji']])
    label = label.reshape(-1)
    return (img, label)


def _sticker_image_to_array(image_content):
    buf = io.BytesIO(image_content)
    img = Image.open(buf)
    if img.width < IMAGE_DROP_SIZE or img.height < IMAGE_DROP_SIZE:
        logger.info('drop small size image {}x{}'.format(
            img.width, img.height))
        raise _DropImageException()
    img = _resize_sticker_image(img, IMAGE_SIZE)
    return np.asarray(img)


def _resize_sticker_image(image, size):
    result = Image.new('RGB', (size, size))
    if image.height > image.width:
        new_height = size
        new_width = int(image.width * size / image.height)
    else:
        new_width = size
        new_height = int(image.height * size / image.width)
    if new_width < IMAGE_DROP_SIZE or new_height < IMAGE_DROP_SIZE:
        logger.info('drop strange aspect ratio size image {}x{}'.format(
            new_width, new_height))
        raise _DropImageException()
    result.paste(image.resize((new_width, new_height)))
    return result


class _DropImageException(Exception):
    pass


class _DropUnrecognizedEmojiException(Exception):
    pass


@functools.lru_cache()
def _get_label_binarizer(emojis):
    label_binarizer = preprocessing.LabelBinarizer()
    label_binarizer.fit(emojis)
    return label_binarizer


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))
