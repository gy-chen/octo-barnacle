
import enum
from octo_barnacle.lock import LockError


class Mark(enum.Enum):
    OK = "OK"
    EMPTY = "EMPTY"
    MISLABEL = "MISLABEL"
    NOT_ANIME = "NOT_ANIME"
    STRANGE_MEME = "STRANGE_MEME"
    OTHER = "OTHER"


class MarkModel:
    """Provide mark stickerset features

    Arguments:
        storage (octo_barnacle.data.mark.storage.MarkStickerStorage)
        mark_lockmanager: (octo_barnacle.data.mark.lockmanager.MarkStickersetLockManager)
    """

    BATCH_SIZE = 12

    def __init__(self, storage, mark_lockmanager):
        self._storage = storage
        self._mark_lockmanager = mark_lockmanager

    def next_batch(self):
        """get next batch stickerset for mark

        batch size default is 12.

        this method does:
            - lock batch stickersets for 180 seconds
            - return locked stickersets and resources (lock values)

        Returns:
            list of dict in format: {
                "sitckerset": sticerset,
                "resource": "stickerset lock value"
            }
        """
        batch = []
        stickersets = self._storage.get_unmark_stickersets()
        while len(batch) != self.BATCH_SIZE:
            try:
                stickerset = next(stickersets)
                resource = self._mark_lockmanager.lock(stickerset['name'])
                batch.append({
                    "stickerset": self._proj_stickerset(stickerset),
                    "resource": resource,
                    "stickers": self.batch_stickers(stickerset['name'])
                })
            except LockError:
                continue
            except StopIteration:
                break
        return batch

    def batch_stickers(self, stickerset_name, limit=7):
        """get small subset of stickers of stickerset

        Arguments:
            stickerset_name (str)
            limit (int)

        Returns:
            list of dict in format {
                "file_id": "image file id",
                "emoji": "emoji"
            }
        """
        stickers = self._storage.get_stickers(stickerset_name, limit)

        return [self._proj_sticker(s) for s in stickers]

    def _proj_sticker(self, sticker):
        return {
            'file_id': sticker['image_id'],
            'emoji': sticker['emoji']
        }

    def _proj_stickerset(self, stickerset):
        return {
            'name': stickerset['name'],
            'title': stickerset['title']
        }

    def mark(self, stickerset_name, mark, resource):
        """mark specific stickerset

        Arguments:
            stickerset_name (str)
            mark (octo_barnacle.data.mark.model.Mark)
            resource (str): lock value obtained by next_batch method 

        Raises:
            ResourceNotAcquiredError: if given resource is not correct or expires
        """
        if not self._mark_lockmanager.is_lock_by(stickerset_name, resource):
            raise ResourceNotAcquiredError()
        self._storage.mark_stickerset(stickerset_name, mark)
        self._mark_lockmanager.unlock(stickerset_name, resource)


class ResourceNotAcquiredError(Exception):
    pass
