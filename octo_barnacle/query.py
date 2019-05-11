import random


class StickerQuery:

    COLLECTION_STICKERS = 'stickers'

    def __init__(self, db):
        """init

        Args:
            db: Mongo database object
        """
        self._db = db

    def find_one_matched_emoji_sticker(self, emoji):
        """find one matched emoji sticker

        if multiple sticker matched, return one randomly

        Args:
            emoji (str): emoji
        Return:
            dict that has field stickerset_name, emoji, image, image_width, image_height, image_path
            None if no matched stickers
        """
        stickers = self._db[self.COLLECTION_STICKERS].find({'emoji': emoji})
        found_count = stickers.count()
        if not found_count:
            return None
        pick_index = random.randint(0, found_count-1)
        return stickers[pick_index]
