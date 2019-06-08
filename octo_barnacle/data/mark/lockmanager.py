from octo_barnacle.lock import LockManager, LockError


class MarkStickersetLockManager(LockManager):
    """Redistributed lock manager for mark stickersets.

    """

    RESOURCE_KEY_FORMAT = 'mark_stickerset:{}'

    def lock(self, stickerset_name):
        return super().lock(self._get_resource_name(stickerset_name))

    def unlock(self, stickerset_name, lock_value):
        super().unlock(self._get_resource_name(stickerset_name), lock_value)

    def is_lock_by(self, stickerset_name, lock_value):
        r_lock_value = self._redis.get(
            self._get_resource_name(stickerset_name))
        if not r_lock_value:
            return False
        return r_lock_value.decode() == lock_value

    def _get_resource_name(self, stickerset_name):
        return self.RESOURCE_KEY_FORMAT.format(stickerset_name)
