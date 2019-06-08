from octo_barnacle.data.mark.storage import MarkStickerStorage


def test_get_unmark(db, sample_stickerset, sample_stickers):
    mark_storage = MarkStickerStorage(db)

    assert len(list(mark_storage.get_unmark_stickersets())) == 0

    mark_storage.store(sample_stickerset, sample_stickers)

    assert len(list(mark_storage.get_unmark_stickersets())) == 1


def test_mark(db, sample_stickerset, sample_stickers):
    mark_storage = MarkStickerStorage(db)

    mark_storage.store(sample_stickerset, sample_stickers)
    mark_storage.mark_stickerset('ChuunibyoudemoKoigaShitai', 'OTHER')

    assert len(list(mark_storage.get_unmark_stickersets())) == 0
