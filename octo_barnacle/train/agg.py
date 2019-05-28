"""Provide functions for analysis stored stikers in mongo

"""


def aggregate_emojis(db):
    """get set of emojis used in stored stickers

    Arguments:
        db (pymongo.database.Database): Mongo database that store stickers

    Returns:
        list of emoji string 
    """
    stickers = db.stickers

    return stickers.distinct("emoji")


def count_emojis(db):
    """count emojis used in stored stickers

    Arguments:
        db (pymongo.database.Database): Mongo database that store stickers

    Returns:
        dict in format { emoji: count, ... }
    """
    stickers = db.stickers

    return stickers.aggregate([
        {"$group": {"_id": "$emoji", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}}
    ])
