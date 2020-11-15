import os
import re


def clean_mongodb_uri(mongodb_uri):
    """Remove username:password."""
    return re.sub(r'//.+@', '//', mongodb_uri)


class Config:
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', 27017)
    DB_NAME = os.environ.get('DB_NAME', 'cars')
    HOST = os.environ.get('HOST', 'localhost')
    PORT = int(os.environ.get('PORT', 5000))
    MONGODB_URI = f'mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}'
    DEBUG = bool(os.environ.get('DEBUG', False))

    @property
    def base_url(self):
        return f"http://{self.HOST}:{self.PORT}"

    def __str__(self) -> str:
        return f'mongodb_uri={clean_mongodb_uri(self.MONGODB_URI)}, debug={self.DEBUG}'


class TestConfig(Config):

    def make_default_test_uri(self):
        return f'mongodb://{self.DB_HOST}:{self.DB_PORT}/items_test'

    MONGODB_URI = os.environ.get('MONGODB_TEST_URI', make_default_test_uri)
    DEBUG = True


config = Config()