"""Provides telegram bot handlers

functions:
  - collect_sticker: collect sticker set of sticker sent by user

"""
import io
import logging
from telegram.ext import MessageHandler, Filters
from octo_barnacle.model import collect_stickerset, CollectStickerSetError
from octo_barnacle.bot.context import get_storage, get_lock_manager, get_sticker_query
from octo_barnacle.bot.filters import FilterEmoji, FilterSymbol

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


def send_random_emoji_sticker(update, context):
    """random choice sticker that matched emoji sent by user"""
    storage = get_storage()
    sticker_query = get_sticker_query()
    emoji = update.message.text
    sticker = sticker_query.find_one_matched_emoji_sticker(emoji)
    if sticker:
        buf = io.BytesIO(sticker['image'])
        update.message.reply_sticker(buf)
    else:
        # TODO add i18n
        update.message.reply_text('今天天氣真好')


def get_handlers():
    """Get handlers that required to make sticker collect bot.

    Returns:
        list of telegram.ext.handler.Handler
    """
    collect_sticker_handler = MessageHandler(Filters.sticker, collect_sticker)
    send_random_emoji_sticker_handler = MessageHandler(
        FilterEmoji(), send_random_emoji_sticker)
    send_random_symbol_sticker_handler = MessageHandler(
        FilterSymbol(), send_random_emoji_sticker
    )
    return [
        collect_sticker_handler,
        send_random_emoji_sticker_handler,
        send_random_symbol_sticker_handler
    ]
