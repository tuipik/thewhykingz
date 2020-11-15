import aioreloader
from aiohttp import web
from db import setup_mongo
from models import ensure_indexes
from views import routes
import config as c


def init(config: c.Config) -> web.Application:
    app = web.Application()
    app['config'] = config
    app.on_startup.append(setup_mongo)
    app.on_startup.append(ensure_indexes)
    app.add_routes(routes)
    aioreloader.start()
    return app


if __name__ == '__main__':
    app = init(c.config)
    web.run_app(app, port=c.config.PORT)
