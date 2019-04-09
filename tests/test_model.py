import hashlib
import pytest
from octo_barnacle.bot import get_bot
from octo_barnacle import model


@pytest.fixture
def bot():
    return get_bot()


def test_get_stickerset(bot):
    stickerset = model._get_stickerset(bot, 'python')
    assert stickerset['name'] == 'Python'
    assert stickerset['title'] == 'Python'

def test_get_stickers(bot):
    stickers = list(model._get_stickers(bot, 'python'))
    assert len(stickers) == 1
    sticker = stickers[0]
    assert sticker['stickerset_name'] == 'Python'
    assert sticker['emoji'] == '🐍'
    assert hashlib.md5(sticker['image']).hexdigest() == '2c5feb400b16bf73c47a68bfd4512181'
    assert sticker['image_path'].startswith('https://api.telegram.org/file/bot')
    assert sticker['image_path'].endswith('stickers/file_0.webp')

    