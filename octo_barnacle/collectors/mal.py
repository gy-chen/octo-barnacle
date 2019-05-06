"""Functions for collect stickers from MyAnimeList recommendations


"""
import csv
import os
import logging
import fasteners
import octo_barnacle.data.mal
from telegram import Bot
from telegram.error import BadRequest
from pymongo import MongoClient
from redis import Redis
from octo_barnacle import model
from octo_barnacle import lock
from octo_barnacle import storage
from .config import MalCollectorConfig

logger = logging.getLogger(__name__)


def main(config=MalCollectorConfig):
    """Try to find stickers that title match MAL recommendations 

    1. download MAL recommendations if not downloaded yet. (or force download setting is enabled)
    2. try to find sticker that title matchs MAL recommendtaions
    3. store found stickers in specific mongo db

    Arguments:
        config (octo_barnacle.config.MalCollectorConfig)
    """
    logging.basicConfig(level=logging.INFO)
    os.makedirs(config.WORK_DIR, exist_ok=True)
    os.chdir(config.WORK_DIR)
    bot = Bot(token=config.BOT_TOKEN)
    db = MongoClient(config.MONGO_CONFIG.HOST, config.MONGO_CONFIG.PORT)[
        config.MONGO_CONFIG.DB]
    storage_ = storage.StickerStorage(db)
    r = Redis(
        host=config.REDIS_CONFIG.HOST,
        port=config.REDIS_CONFIG.PORT
    )
    lock_manager = lock.LockManager(r)
    pid_lock = fasteners.InterProcessLock('mal_pid')
    if not pid_lock.acquire(blocking=False):
        logger.warn('other mal collector is running.')
        return
    with pid_lock:
        logger.info('start mal collector')
        _download_mal_recommendations(
            config.DOWNLOAD_DELAY, config.MAL_FILENAME, config.FORCE_DOWNLOAD)
        for recommendation in _open_mal_recommendations(config.MAL_FILENAME):
            _collect_stickerset(bot, storage_, lock_manager,
                                recommendation['from']['title'])
            _collect_stickerset(bot, storage_, lock_manager,
                                recommendation['to']['title'])
        logger.info('finish mal collector')


def _collect_stickerset(bot, storage, lock_manager, stickerset_name):
    try:
        model.collect_stickerset(bot, storage, lock_manager, stickerset_name)
        logger.info("collected {}".format(stickerset_name))
    except BadRequest:
        logger.debug('cannot found stickerset {}'.format(stickerset_name))
    except lock.LockError:
        logger.info(
            'searched {} before, ignore it now.'.format(stickerset_name))
    except:
        logging.exception(
            'encounter error while collect stickerset {}'.format(stickerset_name))


def _download_mal_recommendations(download_delay, path, force):
    """Fetch MAL recommendation and save to disk

    Saved file format is csv.

    By default, skip the download operation if target path exists. This behavior can be
    override by force argument

    Args:
        - path: path to save file
        - force (bool): set to True if want to download even target path exists.
    """
    if os.path.exists(path) and not force:
        logging.info('skip download because {} exists.'.format(path))
        return

    logger.info('start to download MAL recommendations')
    pager = octo_barnacle.data.mal.RecommendationPager(download_delay)
    parser = octo_barnacle.data.mal.RecommendationParser()
    with open(path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for page, content in enumerate(pager):
            logger.debug(
                'download MAL recommendations page {} content'.format(page))
            for recommendation in parser.parse(content):
                csvwriter.writerow([
                    recommendation['from']['title'],
                    recommendation['from']['img_link'],
                    recommendation['to']['title'],
                    recommendation['to']['img_link'],
                    recommendation['description']
                ])
    logger.info('downloaded MAL recommendations')


def _open_mal_recommendations(path):
    "Open saved mal recommendtions, return iterable that yield recommendation"
    with open(path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            yield {
                'from': {
                    'title': row[0],
                    'img_link': row[1]
                },
                'to': {
                    'title': row[2],
                    'img_link': row[3]
                },
                'description': row[4]
            }
