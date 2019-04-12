"""Provide telegram bot related features

Functions:
  - get_bot()
  - get_updater()

"""
import os
from telegram import Bot
from telegram.ext import Updater
from dotenv import load_dotenv
from octo_barnacle.bot.handlers import get_handlers

load_dotenv()


def get_bot():
    """Get telegram bot object.

    This function will initialize telegram bot with token that received from enviroment.

    Returns:
      telegram.Bot: python-telegram-bot object
    """
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    return bot


def get_updater():
    """Get telegram updater

    This will be entry of starting sticker collect bot.

    Return:
      telegram.ext.updater.Updater
    """
    updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)
    for handler in get_handlers():
        updater.dispatcher.add_handler(handler)
    return updater
