"""Functions for collect stickers from MyAnimeList recommendations


"""
import csv
import os
import logging
import functools
import fasteners
import octo_barnacle.data.mal
import octo_barnacle.data.downloader
from telegram import Bot
from pymongo import MongoClient
from redis import Redis
from octo_barnacle import model
from octo_barnacle import lock
from octo_barnacle import storage
from .config import MalCollectorConfig
from . import utils

logger = logging.getLogger(__name__)


def main(config=MalCollectorConfig):
    """Try to find stickers that title match MAL recommendations 

    1. download MAL recommendations if not downloaded yet. (or force download setting is enabled)
    2. try to find sticker that title matchs MAL recommendtaions
    3. store found stickers in specific mongo db

    Arguments:
        config (octo_barnacle.config.MalCollectorConfig)
    """
    # TODO maybe load level config from enviroment
    logging.basicConfig(level=logging.DEBUG)
    os.makedirs(config.WORK_DIR, exist_ok=True)
    os.chdir(config.WORK_DIR)
    bot = _get_bot(config)
    storage_ = _get_storage(config)
    lock_manager = _get_lock_manager(config)
    downloader = _get_downloader(config)
    pid_lock = fasteners.InterProcessLock('mal_pid')
    if not pid_lock.acquire(blocking=False):
        logger.warn('other mal collector is running.')
        return
    with pid_lock:
        logger.info('start mal collector')
        _download_mal_recommendations(
            downloader, config.MAL_FILENAME, config.FORCE_DOWNLOAD)
        for title in _gen_recommendation_titles(_open_mal_recommendations(config.MAL_FILENAME)):
            logger.info('try to collect {}'.format(title))
            _collect_stickerset(bot, storage_, lock_manager, title)
    logger.info('finish mal collector')


def _get_bot(config=MalCollectorConfig):
    return Bot(token=config.BOT_TOKEN)


def _get_storage(config=MalCollectorConfig):
    db = MongoClient(config.MONGO_CONFIG.HOST, config.MONGO_CONFIG.PORT)[
        config.MONGO_CONFIG.DB]
    return storage.StickerStorage(db)


def _get_lock_manager(config=MalCollectorConfig):
    r = Redis(
        host=config.REDIS_CONFIG.HOST,
        port=config.REDIS_CONFIG.PORT
    )
    return lock.LockManager(r)


def _get_downloader(config=MalCollectorConfig):
    return octo_barnacle.data.downloader.Downloader(config.DOWNLOAD_DELAY)


def _collect_stickerset(bot, storage, lock_manager, stickerset_name):
    try:
        model.collect_stickerset(bot, storage, lock_manager, stickerset_name)
        logger.info("collected {}".format(stickerset_name))
    except model.StickerSetNotFoundError:
        logger.info('cannot found stickerset {}'.format(stickerset_name))
    except lock.LockError:
        logger.info(
            'searched {} before, ignore it now.'.format(stickerset_name))
    except Exception:
        logging.exception(
            'encounter error while collect stickerset {}'.format(stickerset_name))


def _download_mal_recommendations(downloader, path, force):
    """Fetch MAL recommendation and save to disk

    Saved file format is csv.

    By default, skip the download operation if target path exists. This behavior can be
    override by force argument

    Args:
        - downloader (octo_barnacle.data.downloader.Downloader): for downloading content
        - path (str): path to save file
        - force (bool): set to True if want to download even target path exists.
    """
    if os.path.exists(path) and not force:
        logging.info('skip download because {} exists.'.format(path))
        return

    logger.info('start to download MAL recommendations')
    pager = octo_barnacle.data.mal.RecommendationPager(downloader)
    parser = octo_barnacle.data.mal.RecommendationParser()
    with open(path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for page, content in enumerate(pager):
            logger.info(
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


def _gen_recommendation_titles(recommendations):
    """generate titles from recommendation from and to data

    this function also applied some modify to original title:
        - remove punctations
        - remove whitespace
        - try append number

    Args:
        recommendations: iterable of recommendation dict
            {
                'from': {
                    'title': '...',
                    'img_link': '...'
                },
                'to': {
                    'title': '...',
                    'img_link': '...'
                },
                'description': '...'
            }

    Returns:
        iterable of title string
    """
    def gen_titles():
        for recommendation in recommendations:
            yield recommendation['from']['title']
            yield recommendation['to']['title']
    result_gen = gen_titles()
    chain = [
        utils.gen_remove_punctuation,
        utils.gen_remove_whitespace,
        functools.partial(utils.gen_append_range_number, from_=1, to=4)
    ]
    for c in chain:
        result_gen = c(result_gen)
    return result_gen
