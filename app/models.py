from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from bson import ObjectId
from bson.errors import InvalidId

from datetime import datetime
from db import instance

from marshmallow import ValidationError

import schemas
from umongo import Document, fields


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
        indexes = ["-created_time"]


async def ensure_indexes(app: web.Application) -> None:
    await Car.ensure_indexes()


class CarManager:
    @staticmethod
    async def get():
        return [car.dump() async for car in Car.find({})]

    @staticmethod
    async def search(filters):
        search_phrase = filters["q"].lower().strip()
        try:
            car_id = ObjectId(search_phrase)
            return [car.dump() async for car in Car.find({"_id": car_id})]
        except InvalidId:
            return [
                car.dump() async for car in Car.find({"manufacturer": search_phrase})
            ]

    @staticmethod
    async def create(request_body):
        schema = schemas.CarSchema(strict=True)
        try:
            validated_data = schema.load(dict(request_body.items()))
            if validated_data.errors:
                return False, validated_data.errors
            car = Car(**validated_data.data)
            await car.commit()
        except ValidationError as e:
            return False, e.messages
        return True, car

    @staticmethod
    async def get_car_by_id(car_id) -> Car:
        return await Car.find_one({"_id": car_id})

    @staticmethod
    def validate_object_id(object_id):
        try:
            object_id = ObjectId(object_id)
        except InvalidId:
            raise HTTPBadRequest(reason="Invalid id.")
        return object_id

    @staticmethod
    async def update(car_object, request_body):
        schema = schemas.UpdateCarSchema(strict=True)
        try:
            validated_data = schema.load(
                dict(request_body.items()),
                partial=("model", "manufacturer", "colour", "release_year", "vin_code"),
            ).data
        except ValidationError as e:
            return False, e.messages

        car = car_object
        car.update(validated_data)
        car.updated_time = datetime.utcnow()
        await car.commit()
        return True, car

    @staticmethod
    async def delete(car_object):
        car = car_object
        await car.delete()
        return True,
