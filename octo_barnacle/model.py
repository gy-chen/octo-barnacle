import io


def collect_stickerset(bot, stickerset_name):
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
    stickers = [
        {
            'stickerset_name': raw_stickerset.name,
            'emoji': sticker.emoji,
            'image': get_file_binary_content(bot, sticker.file_id)
        }
        for sticker in raw_stickerset.stickers
    ]
    stickerset = {
        'name': raw_stickerset.name,
        'title': raw_stickerset.title,
    }
    # TODO store stickerset


def get_file_binary_content(bot, file_id):
    file_ = bot.get_file(file_id)
    binary_data = io.BytesIO()
    file_.download(out=binary_data)
    return binary_data.value()
