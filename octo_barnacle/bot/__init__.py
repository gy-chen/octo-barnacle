"""Provide telegram bot related features

Functions:
  - get_bot()
  - get_updater()

"""
from telegram.ext import Updater, Bot
from octo_barnacle.bot.handlers import get_handlers


def get_bot():
    """Get telegram bot object.

    This function will initialize telegram bot with token that received from enviroment.

    Returns:
      telegram.Bot: python-telegram-bot object 
    """
    # TODO read token from enviroment
    bot = Bot()
    return bot


def get_updater():
    """Get telegram updater

    This will be entry of starting sticker collect bot.

    Return:
      telegram.ext.updater.Updater
    """
    # TODO read token from entiroment.
    updater = Updater()
    for handler in get_handlers():
        updater.dispatcher.add_handler(handler)
    return updater
