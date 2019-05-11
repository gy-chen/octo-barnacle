"""Provides telegram bot handlers

functions:
  - collect_sticker: collect sticker set of sticker sent by user

"""
import logging
from telegram.ext import MessageHandler, Filters
from octo_barnacle.model import collect_stickerset, CollectStickerSetError
from octo_barnacle.bot.context import get_storage, get_lock_manager

logger = logging.getLogger(__name__)


def collect_sticker(update, context):
    """collect sticker set of sticker sent by user"""
    storage = get_storage()
    lock_manager = get_lock_manager()
    sticker = update.message.sticker
    try:
        collect_stickerset(context.bot, storage,
                           lock_manager, sticker.set_name)
    except CollectStickerSetError as e:
        logger.warn('failed to collect {}'.format(
            sticker.set_name), exc_info=e)


def get_handlers():
    """Get handlers that required to make sticker collect bot.

    Returns:
        list of telegram.ext.handler.Handler
    """
    collect_sticker_handler = MessageHandler(Filters.sticker, collect_sticker)
    return [collect_sticker_handler]
