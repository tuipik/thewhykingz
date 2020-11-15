from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from umongo import ValidationError
import schemas
import services
from config import config


routes = web.RouteTableDef()
BASE_URL = config.base_url


@routes.get('/api/v1/cars')
async def list_cars(request: web.Request) -> web.Response:
    manufacturer = services.get_query_param(request)
    if manufacturer:
        cars = await services.get_manufacturer_cars(manufacturer)
        return web.json_response([car.dump() async for car in cars], status=200)
    cars = await services.get_all_cars()
    return web.json_response([car.dump() async for car in cars], status=200)


@routes.post('/api/v1/cars')
async def create_car(request: web.Request) -> web.Response:
    try:
        schema = schemas.CarSchema(strict=True)
        data = schema.load(await request.json()).data
    except ValidationError as error:
        raise HTTPBadRequest(reason=error.messages)

    car = await services.create_car(data)
    return web.json_response(car.dump(), status=201)


@routes.get(r'/api/v1/cars/{car_id:\w{24}}')
async def get_car(request: web.Request) -> web.Response:
    car_id = services.validate_object_id(request.match_info['car_id'])
    car = await services.get_car_by_id(car_id)

    return web.json_response(car.dump(), status=200)


@routes.put(r'/api/v1/cars/{car_id:\w{24}}')
async def update_car_data(request: web.Request) -> web.Response:
    car_id = services.validate_object_id(request.match_info['car_id'])

    try:
        schema = schemas.UpdateCarSchema(strict=True)
        data = schema.load(await request.json()).data
    except ValidationError as error:
        raise HTTPBadRequest(reason=error.messages)

    car = await services.update_car(car_id, data)

    return web.json_response(car.dump(), status=200)


@routes.delete(r'/api/v1/cars/{car_id:\w{24}}')
async def delete_car(request: web.Request) -> web.Response:
    car_id = services.validate_object_id(request.match_info['car_id'])
    await services.delete_car(car_id)

    return web.json_response({}, status=204)

