"""provide functions for converting stored stickers to tfrecord

"""
import logging
import tensorflow as tf
from .config import ConvertToTfRecordConfig
from . import utils
from . import dataset

logger = logging.getLogger(__name__)


def main(config=ConvertToTfRecordConfig):
    """main function for converting stored stickers into tfrecord file


    """
    logging.basicConfig(level=logging.DEBUG)
    utils.ch_workdir(config.TFRECORD_WORKDIR)
    storage = utils.get_storage(
        config.MONGO_CONFIG.HOST, config.MONGO_CONFIG.PORT, config.MONGO_CONFIG.DB)
    ds = dataset.get_tf_dataset(storage)
    logger.info("start to convert stored stickers to tfrecord")
    with tf.Session() as sess:
        sess.run(dataset.save_tf_dataset(ds, config.TFRECORD_FILENAME))
    logging.info("done converting stored stickers to tfrecord")
