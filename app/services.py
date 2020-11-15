from datetime import datetime
from typing import AsyncIterable, Dict

from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound, HTTPBadRequest
from bson import ObjectId
from bson.errors import InvalidId

from models import Car


async def get_all_cars() -> AsyncIterable[Car]:
    return Car.find({})


async def get_manufacturer_cars(manufacturer: str) -> AsyncIterable[Car]:
    return Car.find({'manufacturer': manufacturer.lower()})


async def create_car(data: Dict) -> Car:
    car = Car(**data)
    await car.commit()
    return car


async def get_car_by_id(car_id: ObjectId) -> Car:
    car = await Car.find_one({'_id': car_id})
    if not car:
        raise HTTPNotFound()

    return car


async def update_car(car_id: ObjectId, data: Dict) -> Car:
    car = await get_car_by_id(car_id)

    car.update(data)
    car.updated_time = datetime.utcnow()
    await car.commit()

    return car


async def delete_car(car_id: ObjectId):
    car = await get_car_by_id(car_id)
    await car.delete()


def validate_object_id(object_id: str) -> ObjectId:
    try:
        object_id = ObjectId(object_id)
    except InvalidId:
        raise HTTPBadRequest(reason='Invalid id.')
    return object_id


def get_query_param(request: web.Request):
    try:
        manufacturer = request.query.getone('manufacturer')
        return manufacturer
    except KeyError:
        return None
