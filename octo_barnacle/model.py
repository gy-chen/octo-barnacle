import io
from functools import lru_cache


def collect_stickerset(bot, storage, stickerset_name):
    """Collect specific stickerset

    This function does:
        - obtain stickerset information from telegram
        - collect sticker file from telegram
        - store stickerset data into storage

    Raises:
        AcquireLockException: if failed to acquire distributed lock

    Args:
        - stickerset_name (str): stickerset name that usually obtained from telegram api
    """
    raw_stickerset = bot.get_sticker_set(stickerset_name)
    stickers = (
        {
            'stickerset_name': raw_stickerset.name,
            'emoji': sticker.emoji,
            'image': _get_file(bot, sticker.file_id)['binary_content'],
            'image_path': _get_file(bot, sticker.file_id)['path']
        }
        for sticker in raw_stickerset.stickers
    )
    stickerset = {
        'name': raw_stickerset.name,
        'title': raw_stickerset.title,
    }
    storage.store(stickerset, stickers)


@lru_cache
def _get_file(bot, file_id):
    file_ = bot.get_file(file_id)
    binary_data = io.BytesIO()
    file_.download(out=binary_data)
    return {
        'path': file_.file_path,
        'binary_content': binary_data.value()
    }
