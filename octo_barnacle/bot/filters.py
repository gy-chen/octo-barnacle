from telegram.ext import BaseFilter
from octo_barnacle.bot.utils import is_emoji, is_symbol


class FilterEmoji(BaseFilter):
    "filter message that only contain single emoji"

    def filter(self, message):
        if not message.text:
            return False
        return is_emoji(message.text)


class FilterSymbol(BaseFilter):
    "filter message that only contain single symbol"

    def filter(self, message):
        if not message.text:
            return False
        return is_symbol(message.text)
