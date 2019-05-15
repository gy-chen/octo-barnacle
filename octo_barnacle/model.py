import io
from telegram.error import BadRequest


class CollectStickerSetError(Exception):
    pass


class StickerSetNotFoundError(CollectStickerSetError):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


def collect_stickerset(bot, storage, lock_manager, stickerset_name):
    """Collect specific stickerset

    This function does:
        - obtain stickerset information from telegram
        - collect sticker file from telegram
        - store stickerset data into storage

    Args:
        - bot (telegram.Bot): python-telegram-bot Bot instance
        - storage (octo_barnacle.storage.StickerStorage): usually obtained by octo_barnacle.storage.get_storage()
        - lock_manager (octo_barnacle.lock.LockManager): usually obtained by octo_barnacle.lock.get_lock_manager()
        - stickerset_name (str): stickerset name that usually obtained from telegram api

    Raises:
        octo_barnacle.lock.LockError: if failed to acquire distributed lock
        StickerSetNotFoundError: if stickerset not found
        StickerSetNotFoundError: if encounter any error while collect stickerset
    """
    lock_val = lock_manager.lock(stickerset_name)

    try:
        stickerset = _get_stickerset(bot, stickerset_name)
        stickers = _get_stickers(bot, stickerset_name)

        storage.store(stickerset, stickers)
    except BadRequest as e:
        raise StickerSetNotFoundError(stickerset_name) from e
    except Exception as e:
        lock_manager.unlock(stickerset_name, lock_val)
        raise CollectStickerSetError from e


def _get_stickerset(bot, stickerset_name):
    raw_stickerset = bot.get_sticker_set(stickerset_name)
    stickerset = {
        'name': raw_stickerset.name,
        'title': raw_stickerset.title,
    }
    return stickerset


def _get_stickers(bot, stickerset_name):
    raw_stickerset = bot.get_sticker_set(stickerset_name)
    for sticker in raw_stickerset.stickers:
        sticker_file = _get_file(bot, sticker.file_id)
        yield {
            'image_id': sticker.file_id,
            'stickerset_name': raw_stickerset.name,
            'emoji': sticker.emoji,
            'image': sticker_file['binary_content'],
            'image_width': sticker.width,
            'image_height': sticker.height,
            'image_path': sticker_file['path']
        }


def _get_file(bot, file_id):
    file_ = bot.get_file(file_id)
    binary_data = io.BytesIO()
    file_.download(out=binary_data)
    return {
        'path': file_.file_path,
        'binary_content': binary_data.getvalue()
    }
