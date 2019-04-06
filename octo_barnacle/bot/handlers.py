"""Provides telegram bot handlers

functions:
  - collect_sticker: collect sticker set of sticker sent by user

"""
from telegram.ext import MessageHandler, Filters
from octo_barnacle.model import collect_stickerset


def collect_sticker(update, context):
    """collect sticker set of sticker sent by user"""
    sticker = update.message.sticker
    collect_stickerset(sticker.set_name)


def get_handlers():
    """Get handlers that required to make sticker collect bot.

    Returns:
        list of telegram.ext.handler.Handler
    """
    collect_sticker_handler = MessageHandler(Filters.sticker, collect_sticker)
    return [collect_sticker_handler]
