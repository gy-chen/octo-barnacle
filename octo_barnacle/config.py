import os
from dotenv import load_dotenv

load_dotenv()


class MongoConfig:

    HOST = os.getenv('MONGO_HOST', 'localhost')
    PORT = int(os.getenv('MONGO_PORT', 27017))
    DB = os.getenv('MONGO_DB', 'octo_barnacle')


class RedisConfig:
    HOST = os.getenv('REDIS_HOST', 'localhost')
    PORT = int(os.getenv('REDIS_PORT', 6379))
