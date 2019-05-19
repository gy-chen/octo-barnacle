"""Collect stickers using MyAnimestList characters data
"""
import csv
import functools
import os
import logging
import fasteners
from octo_barnacle.collectors.config import MalCollectorConfig
from octo_barnacle.collectors import utils
from octo_barnacle.data import mal

logger = logging.getLogger(__name__)


def main(config=MalCollectorConfig):
    """main function for collecting stickers using MyAnimestList characters data"""
    logging.basicConfig(level=logging.DEBUG)
    utils.ch_workdir(config.WORK_DIR)
    bot = utils.get_bot(config.BOT_TOKEN)
    storage = utils.get_storage(
        config.MONGO_CONFIG.HOST, config.MONGO_CONFIG.PORT, config.MONGO_CONFIG.DB)
    lock_manager = utils.get_lock_manager(
        config.REDIS_CONFIG.HOST, config.REDIS_CONFIG.PORT)
    downloader = utils.get_downloader(config.DOWNLOAD_DELAY)
    pid_lock = fasteners.InterProcessLock('mal_characters_pid')
    if not pid_lock.acquire(blocking=False):
        logger.warn('other MAL characters collector is running.')
        return
    with pid_lock:
        _download_mal_characters(
            downloader, config.MAL_FILENAME, config.FORCE_DOWNLOAD)
        for name in _gen_mal_character_name(_open_mal_characters(config.MAL_FILENAME)):
            utils.collect_stickerset(bot, storage, lock_manager, name)


def _download_mal_characters(downloader, path, force):
    """download and save parsed MAL characters result

    ignore downloading if path is exists, set force to True if want to override existing
    path.

    Args:
        downloader (octo_barnacle.data.downloader.Downloader): for downloading content
        path (str): store file path
        force (bool): set to true if want to download even path file exists
    """
    if os.path.exists(path) and not force:
        logger.info('skip download because {} exists.'.format(path))
        return

    pager = mal.CharacterPager(downloader)
    parser = mal.CharacterParser()

    with open(path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for page, content in enumerate(pager):
            logger.info(
                'download MAL character page {} content'.format(page))
            for ranking in parser.parse(content):
                csvwriter.writerow([
                    ranking['people']['name'],
                    ranking['people']['img_link'],
                    ranking['rank'],
                    '::::'.join(ranking['animeography']),
                    '::::'.join(ranking['mangaography']),
                    ranking['favorites']
                ])
    logger.info('downloaded MAL characters')


def _open_mal_characters(path):
    """open saved mal characters and yield result one by one

    Args:
        path (str): stored MAL characters file path

    Return:
        iterable that yield characters one by one
    """
    with open(path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            yield {
                'people': {
                    'name': row[0],
                    'img_link': row[1]
                },
                'rank': int(row[2]),
                'animeography': row[3].split('::::'),
                'mangaography': row[4].split('::::'),
                'favorites': int(row[5])
            }


def _gen_mal_character_name(mal_characters):
    """yield character name from given MAL characters

    steps of processing name:
        - remove white and punctuation
        - append name with '', '1', '2', '3', and '4'

    Examples:
        _gen_mal_character_name(mal_characters) -> yield name, name1, name2, name3, etc...

    Args:
        mal_characters: iterable that generate MAL character in format
            {
                'people': {
                    'name': 'character name',
                    'img_link': 'character image link'
                },
                'rank': rank number,
                'animeography': [
                    'anime name',
                    ...
                ],
                'mangaography': [
                    'manga name',
                    ...
                ],
                'favorites': favorites number
            }

    Returns:
        iterable of character name
    """
    gen_names = (ranking['people']['name'] for ranking in mal_characters)
    chain = [
        utils.gen_remove_nonascii,
        utils.gen_remove_whitespace,
        utils.gen_remove_punctuation,
        functools.partial(utils.gen_append_range_number, from_=1, to=4)
    ]
    result_gen = gen_names
    for c in chain:
        result_gen = c(result_gen)
    return result_gen
