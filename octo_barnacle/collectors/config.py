import os
import dotenv
from ..config import MongoConfig
from ..config import RedisConfig

dotenv.load_dotenv()


class MalCollectorConfig:
    BOT_TOKEN = os.getenv('MAL_BOT_TOKEN')
    MONGO_CONFIG = MongoConfig
    REDIS_CONFIG = RedisConfig
    FORCE_DOWNLOAD = bool(
        eval(os.getenv('MAL_COLLECTOR_FORCE_DOWNLOAD', 'False')))
    DOWNLOAD_DELAY = int(os.getenv('MAL_COLLECTOR_DOWNLOAD_DELAY', 3))
    WORK_DIR = os.path.expanduser(os.getenv('MAL_COLLECTOR_WORKDIR', './'))
    MAL_FILENAME = os.getenv('MAL_COLLECTOR_FILENAME', 'mal.csv')
