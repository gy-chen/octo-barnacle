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
    # TODO search for better place for dev dependency
    'pyrogram'
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
)
