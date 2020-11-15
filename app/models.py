from aiohttp import web
from datetime import datetime
from umongo import Document, fields
from db import instance


@instance.register
class Car(Document):
    model = fields.StringField()
    manufacturer = fields.StringField()
    release_year = fields.IntegerField()
    colour = fields.StringField()
    vin_code = fields.StringField(unique=True)
    created_time = fields.DateTimeField(default=datetime.utcnow)
    updated_time = fields.DateTimeField()

    class Meta:
        indexes = ['-created_time']


async def ensure_indexes(app: web.Application) -> None:
    await Car.ensure_indexes()
