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
        self._db[self.COLLECTION_STICKERSET].update(
            {'name': stickerset['name']},
            stickerset,
            {
                'upsert': True
            }
        )
        self._db[self.COLLECTION_STICKERS].delete_many(
            {'stickerset_name': stickerset.name})
        for sticker in stickers:
            self._db[self.COLLECTION_STICKERS].insert(sticker)
