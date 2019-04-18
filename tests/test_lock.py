import os
import dotenv
import pytest
from redis import Redis
from octo_barnacle.lock import LockManager, LockError

dotenv.load_dotenv()


@pytest.fixture
def redis():
    r = Redis(
        host=os.environ.get('TEST_REDIS_HOST'),
        port=os.environ.get('TEST_REDIS_PORT')
    )
    yield r
    r.flushdb()


@pytest.fixture
def lock_manager(redis):
    return LockManager(redis)


def test_lock(lock_manager):
    resource = 'test'
    lock_value = lock_manager.lock(resource)
    assert lock_value is not None

    with pytest.raises(LockError):
        lock_manager.lock(resource)


def test_unlock(lock_manager):
    resource = 'test'
    lock_value = lock_manager.lock(resource)

    lock_manager.unlock(resource, lock_value)

    assert lock_manager.lock(resource) is not None
