import os
import dotenv

dotenv.load_dotenv()


class RedisConfig:
    HOST = os.getenv('MARK_REDIS_HOST', '127.0.0.1')
    PORT = int(os.getenv('MARK_REDIS_PORT', 6379))


class MongoConfig:
    HOST = os.getenv('MARK_MONGO_HOST', '127.0.0.1')
    PORT = int(os.getenv('MARK_MONGO_PORT', 27017))
    DB = os.getenv('MARK_MONGO_DB', 'octo_barnacle')


class WebConfig:
    MARK_BOT_TOKEN = os.getenv('MARK_BOT_TOKEN', None)
    MARK_REDIS_HOST = RedisConfig.HOST
    MARK_REDIS_PORT = RedisConfig.PORT
    MARK_MONGO_HOST = MongoConfig.HOST
    MARK_MONGO_PORT = MongoConfig.PORT
    MARK_MONGO_DB = MongoConfig.DB
