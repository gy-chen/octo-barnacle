import string
import os
import logging
from telegram import Bot
from pymongo import MongoClient
from redis import Redis
from octo_barnacle import lock
from octo_barnacle import storage
from octo_barnacle import model
from octo_barnacle.data import downloader

logger = logging.getLogger(__name__)

_trans_remove_punctuation = str.maketrans('', '', string.punctuation)
_trans_remove_whitespace = str.maketrans('', '', string.whitespace)


def gen_remove_punctuation(str_gen):
    """remove punctuation of string from given generator

    Arguments:
        str_gen: expect string iterable

    Return:
        generator that generate string
    """
    return (s.translate(_trans_remove_punctuation) for s in str_gen)


def gen_remove_whitespace(str_gen):
    """remove whitespace of string from given generator

    Arguments:
        str_gen: expect string iterable

    Return:
        generator that generate string
    """
    return (s.translate(_trans_remove_whitespace) for s in str_gen)


def gen_append_range_number(str_gen, from_, to):
    """append number to string from given generator

    beside generate string that appended number, it also generate original string.

    e.g. gen_append_range_number('aaa', 1, 1) -> ('aaa', 'aaa1')

    Arguments:
        str_gen: expect string iterable
        from_: start of appendix number range 
        to: end of appendix number range (include)

    Return:
        generator that generate string
    """
    for s in str_gen:
        yield s
        for num in range(from_, to+1):
            yield '{}{}'.format(s, num)


def gen_remove_nonascii(str_gen):
    """remove nonascii character

    Arguments:
        str_gen: string iterable

    Return:
        generator that generate string
    """
    for s in str_gen:
        yield ''.join(c for c in s if c.isascii())


def ch_workdir(workdir):
    os.makedirs(workdir, exist_ok=True)
    os.chdir(workdir)


def get_bot(token):
    return Bot(token)


def get_storage(host, port, db):
    db = MongoClient(host, port)[db]
    return storage.StickerStorage(db)


def get_lock_manager(host, port):
    r = Redis(host, port)
    return lock.LockManager(r)


def get_downloader(delay):
    return downloader.Downloader(delay)


def collect_stickerset(bot, storage, lock_manager, stickerset_name):
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
