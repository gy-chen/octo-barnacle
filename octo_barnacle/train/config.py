import os
from ..config import MongoConfig


class ConvertToTfRecordConfig:
    MONGO_CONFIG = MongoConfig
    TFRECORD_WORKDIR = os.getenv('TF_TFRECORD_WORKDIR', '.')
    TFRECORD_FILENAME = os.getenv('TF_TFRECORD_FILENAME', 'stickers.tfrecord')
