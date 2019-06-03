from io import open

from setuptools import find_packages, setup

with open('octo_barnacle/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

REQUIRES = [
    'python-telegram-bot==12.0.0b1',
    'pymongo',
    'python-dotenv',
    'redis',
    'requests',
    'beautifulsoup4',
    'fasteners',
    'flask'
]

setup(
    name='octo-barnacle',
    version=version,
    description='A telegram bot and web api for collecting telegram stickers',
    author='GYCHEN',
    author_email='gy.chen@gms.nutc.edu.tw',
    maintainer='GYCHEN',
    maintainer_email='gy.chen@gms.nutc.edu.tw',
    url='https://github.com/gy-chen/octo-barnacle',
    install_requires=REQUIRES,
    tests_require=['pytest'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'octo-barnacle-collect-mal-recommendation=octo_barnacle.collectors.mal:main',
            'octo-barnacle-collect-mal-characters=octo_barnacle.collectors.mal_character:main',
            'octo-barnacle-bot=octo_barnacle.bot:main',
            'octo-barnacle-stored-stickers-to-tfrecord=octo_barnacle.train.convert:main'
        ],
    },
)
