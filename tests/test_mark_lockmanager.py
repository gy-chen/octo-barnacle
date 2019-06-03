from octo_barnacle.data.mark.lockmanager import MarkStickersetLockManager, LockError


def test_lock(redis):
    lock_manager = MarkStickersetLockManager(redis)

    assert not lock_manager.is_lock_by('Python', '')

    lock_value = lock_manager.lock('Python')

    assert lock_manager.is_lock_by('Python', lock_value)
    assert not lock_manager.is_lock_by('Python', '4413')

    lock_manager.unlock('Python', lock_value)
    assert not lock_manager.is_lock_by('Python', lock_value)
