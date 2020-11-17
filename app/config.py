import os


class Config:
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", 27017)
    DB_NAME = os.environ.get("DB_NAME", "cars")
    HOST = os.environ.get("HOST", "localhost")
    PORT = int(os.environ.get("PORT", 5000))
    MONGODB_URI = f"mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}"
    DEBUG = bool(os.environ.get("DEBUG", False))

    @property
    def BASE_URL(self):
        return f"http://{self.HOST}:{self.PORT}"


config = Config()

