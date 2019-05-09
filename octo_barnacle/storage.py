import logging
from pymongo.errors import InvalidOperation

logger = logging.getLogger(__name__)


class StickerStorage:
    """Store sticker set and stickers"""

    COLLECTION_STICKERSET = 'stickerset'
    COLLECTION_STICKERS = 'stickers'

    def __init__(self, db):
        """init

        Args:
            db: Mongo database object
        """
        self._db = db

    def store(self, stickerset, stickers):
        """Store given stickerset and stickers

        Args:
          stickerset (dict): expect has fields name, and title
          stickers (list): expect item of list has fields stickerset_name, emoji, 
            image, image_width, image_height, and image_path
        """
        self._db[self.COLLECTION_STICKERSET].update_one(
            {'name': stickerset['name']},
            {
                '$set': stickerset
            },
            upsert=True
        )
        self._db[self.COLLECTION_STICKERS].delete_many(
            {'stickerset_name': stickerset['name']})
        try:
            self._db[self.COLLECTION_STICKERS].insert_many(stickers)
        except (InvalidOperation, TypeError):
            logger.warning(
                'insert empty stickers of stickerset {}'.format(stickerset['name']))

    def get_stickersets(self):
        """Get stored stickersets.

        Returns:
          iterable of stickersets
        """
        return self._db[self.COLLECTION_STICKERSET].find()

    def get_stickers(self, stickerset_name=None):
        """Get stored stickers

        Args:
          stickerset_name (str | None)

        Returns:
          iterable of stickers
        """
        if stickerset_name is None:
            return self._db[self.COLLECTION_STICKERS].find()
        return self._db[self.COLLECTION_STICKERS].find({'stickerset_name': stickerset_name})
