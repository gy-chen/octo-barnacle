import uuid
import datetime


class LockManager:
    def __init__(self, redis, default_expires=None):
        self._redis = redis
        self._default_expires = default_expires or int(
            datetime.timedelta(days=30).total_seconds())

    def lock(self, resource, expires=None):
        """lock specific resource

        Args:
            resource (str): resource name
            expires (int): lock expire time in seconds

        Raises:
            LockError

        Returns:
            string for unlocking the resource
        """
        expires = expires or self._default_expires
        lock_value = self._generate_lock_value()
        acquire_result = self._redis.set(
            resource, lock_value, ex=expires, nx=True)
        if acquire_result is None:
            raise LockError()
        return lock_value

    def unlock(self, resource, lock_value):
        """Unlock specific resource

        Args:
            resource (str): resource name
            lock_value (str): value that retrived from lock return value
        """
        if self._redis.get(resource).decode() == lock_value:
            self._redis.delete(resource)

    def _generate_lock_value(self):
        return uuid.uuid1().hex


class LockError(Exception):
    pass
