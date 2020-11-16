import aiohttp_jinja2
from aiohttp import web

from models import CarManager


@aiohttp_jinja2.template("index.html")
async def index(request):
    if request.query:
        return {"cars": await CarManager.search(request.query)}
    return {"cars": await CarManager.get()}


@aiohttp_jinja2.template("detail_car.html")
async def car_detail(request):
    car_id = request.match_info["car_id"]
    validated_car_id = CarManager.validate_object_id(car_id)
    car = await CarManager.get_car_by_id(validated_car_id)
    return {"car": car.dump()}


@aiohttp_jinja2.template("create_car.html")
async def create_car(request):

    if request.method == "POST":
        request_body = await request.post()
        created, data = await CarManager.create(request_body)
        if created:
            return aiohttp_jinja2.render_template(
                "detail_car.html", request, context={"car": data.dump(), "error": {}}
            )
        return aiohttp_jinja2.render_template(
            "create_car.html", request, context={"car": request_body, "errors": data}
        )
    return {
        "car": {
            "manufacturer": "",
            "model": "",
            "colour": "",
            "release_year": "",
            "vin_code": "",
        },
        "errors": {},
    }


@aiohttp_jinja2.template("update_car.html")
async def update_car(request):
    car_id = request.match_info["car_id"]
    validated_car_id = CarManager.validate_object_id(car_id)
    car = await CarManager.get_car_by_id(validated_car_id)
    return {"car": car.dump(), "errors": {}}


@aiohttp_jinja2.template("update_car.html")
async def update_car_apply(request):
    if request.method == "POST":
        car_id = CarManager.validate_object_id(request.match_info["car_id"])
        car = await CarManager.get_car_by_id(car_id)
        request_body = await request.post()
        updated, data = await CarManager.update(car, request_body)
        if updated:
            return aiohttp_jinja2.render_template(
                "detail_car.html", request, context={"car": data.dump(), "error": data}
            )
        response_car = {**request_body, "id": str(car_id)}
        return aiohttp_jinja2.render_template(
            "update_car.html", request, context={"car": response_car, "errors": data}
        )


async def delete_car(request):
    car_id = request.match_info["car_id"]
    validated_car_id = CarManager.validate_object_id(car_id)
    car = await CarManager.get_car_by_id(validated_car_id)
    deleted = {"car": await CarManager.delete(car)}
    raise web.HTTPSeeOther(location=f"/")
