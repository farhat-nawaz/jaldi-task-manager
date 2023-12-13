import enum
import os
from dotenv import load_dotenv

load_dotenv()


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Config:
    # App vars
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = False
    LOG_LEVEL = LogLevel.INFO
    ENVIRONMENT = "production"

    # Database vars
    PONY = {
        'provider': 'mysql',
        'host': os.environ["DB_HOST"],
        'user': os.environ["DB_USER"],
        "passwd": os.environ["DB_PASSWORD"],
        "db": os.environ["DB_NAME"]
    }


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    # App vars
    HOST = "127.0.0.1"
    PORT = 8000
    DEBUG = True
    LOG_LEVEL = LogLevel.DEBUG
    ENVIRONMENT = "development"
    


