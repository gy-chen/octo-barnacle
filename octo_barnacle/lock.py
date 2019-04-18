class LockManager:
    def __init__(self, redis):
        self._redis = redis

    def lock(self, resource, expires=86400):
        """lock specific resource

        Args:
            resource (str): resource name
            expires (int): lock expire time in seconds 

        Raises:
            LockException

        Returns:
            string for unlocking the resource
        """
        # TODO
        pass

    def unlock(self, lock):
        """Unlock specific resource

        Args:
            lock (str): value that retrived from lock return value
        """
        # TODO
        pass
