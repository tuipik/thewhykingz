import aiohttp_jinja2
import aioreloader
import jinja2
from aiohttp import web
from db import setup_mongo
from models import ensure_indexes
import config as c
from routers import setup_routes


def init(config: c.Config) -> web.Application:
    app = web.Application()
    app["config"] = config
    app.on_startup.append(setup_mongo)
    app.on_startup.append(ensure_indexes)
    setup_routes(app)
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader("main"),
    )

    aioreloader.start()
    return app


if __name__ == "__main__":
    app = init(c.config)
    web.run_app(app, port=c.config.PORT)
