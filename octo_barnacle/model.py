import io


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
    stickerset = _get_stickerset(bot, stickerset_name)
    stickers = _get_stickers(bot, stickerset_name)

    storage.store(stickerset, stickers)


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
