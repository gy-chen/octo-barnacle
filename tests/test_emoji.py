from octo_barnacle.train.emoji import get_emoji_codepoints, predefined


def test_main():
    emojis = get_emoji_codepoints()
    assert emojis == predefined.emojis
