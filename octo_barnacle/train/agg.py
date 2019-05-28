"""Provide functions for analysis stored stikers in mongo

"""
import functools
import heapq


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


def most_common_emojis(db, limit=10):
    """get top most common emojis in stored stickers

    Arguments:
        db (pymongo.database.Database): Mongo database that store stickers
        limit (int): number of return emojis

    Returns:
        list of emoji, length is equal or less than limit
    """
    emojis_count = count_emojis(db)

    @functools.total_ordering
    class _OrderByCount:

        def __init__(self, emoji_count):
            self.emoji_count = emoji_count

        def __eq__(self, other):
            return self.emoji_count['total'] == other.emoji_count['total']

        def __lt__(self, other):
            return self.emoji_count['total'] > other.emoji_count['total']

    pq = []

    for emoji_count in emojis_count:
        heapq.heappush(pq, _OrderByCount(emoji_count))

    result = []
    for _ in range(limit):
        try:
            result.append(heapq.heappop(pq).emoji_count['_id'])
        except IndexError:
            break
    return result
