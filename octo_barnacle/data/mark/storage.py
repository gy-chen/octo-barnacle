from octo_barnacle.storage import StickerStorage


class MarkStickerStorage(StickerStorage):

    def get_unmark_stickersets(self):
        return self._db[self.COLLECTION_STICKERSET].find({
            'mark': {'$exists': False}
        })

    def mark_stickerset(self, stickerset_name, mark):
        self._db[self.COLLECTION_STICKERSET].find_one_and_update(
            {'name': stickerset_name},
            {'$set': {'mark': mark}}
        )
