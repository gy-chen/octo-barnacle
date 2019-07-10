from octo_barnacle.storage import StickerStorage


class MarkStickerStorage(StickerStorage):

    def __init__(self, db):
        super().__init__(db)
        self._db[self.COLLECTION_STICKERSET].create_index('mark')

    def get_unmark_stickersets(self):
        return self._db[self.COLLECTION_STICKERSET].find({
            'mark': {'$exists': False}
        })

    def get_stickers(self, stickerset_name, limit=7):
        """get small subset of stickers of stickerset

        Arguments:
            stickerset_name (str)
            limit (int)

        Returns:
            list of sticker
        """
        return self._db[self.COLLECTION_STICKERS].find({
            "stickerset_name": stickerset_name
        }).limit(limit)

    def mark_stickerset(self, stickerset_name, mark):
        self._db[self.COLLECTION_STICKERSET].find_one_and_update(
            {'name': stickerset_name},
            {'$set': {'mark': mark}}
        )
