import argparse
import subprocess
from . import conftest
from octo_barnacle import storage
from octo_barnacle import model


def collect_sample_stickers(bot, db, stickerset_name):
    """collect sample stickers to test database

    Arguments:
        db (Mongo DB)
    """
    stickerset = model._get_stickerset(bot, stickerset_name)
    stickers = model._get_stickers(bot, stickerset_name)
    stge = storage.StickerStorage(db)
    stge.store(stickerset, stickers)


def export_sample_stickers(db, path):
    """export stickers in the db

    Arguments:
        db (Mongo DB)
        path (str)
    """
    host, port = db.client.HOST, db.client.PORT
    subprocess.run(
        [
            'mongodump',
            '--host',
            f'{host}:{port}',
            '--db',
            f'{db.name}',
            f'--out={path}'
        ],
        check=True
    )


def _get_fixture(fixture):
    try:
        return next(fixture)
    except TypeError:
        return fixture


def _teardown(fixture):
    try:
        while True:
            next(fixture)
    except StopIteration:
        pass
    except TypeError:
        pass


def main_collect_export_sample(path, name, **_):
    bot_fixture = conftest.bot.__wrapped__()
    db_fixture = conftest.db.__wrapped__()
    bot = _get_fixture(bot_fixture)
    db = _get_fixture(db_fixture)

    collect_sample_stickers(bot, db, name)
    export_sample_stickers(db, path)

    _teardown(bot)
    _teardown(db)


def get_arg_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    collect_sample_parser = subparsers.add_parser('collect_sample',
                                                  help='collect and export sample stickerset and stickers')
    collect_sample_parser.add_argument(
        'path', help='directory path to store exported data')
    collect_sample_parser.add_argument(
        '--name',
        default='ChuunibyoudemoKoigaShitai',
        help='sample stickerset name to collect'
    )

    collect_sample_parser.set_defaults(func=main_collect_export_sample)

    return parser


if __name__ == '__main__':
    parser = get_arg_parser()
    args = parser.parse_args()
    args.func(**args.__dict__)

