class LockManager:
    def __init__(self, redis):
        self._redis = redis

    def lock(self, resource, expires=86400):
        """lock specific resource

        Args:
            resource (str): resource name
            expires (int): lock expire time in seconds 

        Returns:
            True if lock successfully, False otherwise
        """
        # TODO
        pass

    def unlock(self, resource):
        """Unlock specific resource

        Args:
            resource (str): resource name
        """
        # TODO
        pass
