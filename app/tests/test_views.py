from aiohttp.test_utils import unittest_run_loop

from aiohttp.test_utils import AioHTTPTestCase

from main import init
from models import Car
import os

from schemas import CarSchema


class TestingConfig:
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", 27017)
    DB_NAME = os.environ.get("DB_NAME", "cars")
    HOST = os.environ.get("HOST", "localhost")
    PORT = int(os.environ.get("PORT", 5000))
    MONGODB_URI = f"mongodb://{DB_HOST}:{DB_PORT}/test_db"
    DEBUG = True

    @property
    def BASE_URL(self):
        return f"http://{self.HOST}:{self.PORT}"

    def __str__(self) -> str:
        return f"mongodb_uri={self.MONGODB_URI}, debug={self.DEBUG}"


conf = TestingConfig()

CAR_DATA = {
    "manufacturer": "Ford",
    "model": "Kuga",
    "colour": "white",
    "release_year": 2019,
    "vin_code": "XW0BF8HK40S010001",
}


class AppTestCase(AioHTTPTestCase):
    async def get_application(self):
        return init(conf)

    async def tearDownAsync(self) -> None:
        await self.app["db"].client.drop_database(self.app["db"])


async def create_car(data):
    schema = CarSchema(strict=True)
    validated_data = schema.load(data)
    car = Car(**validated_data.data)
    await car.commit()


class ViewsTestCase(AppTestCase):
    @unittest_run_loop
    async def test_data_on_base_page(self):
        await create_car(CAR_DATA)

        resp = await self.client.get("/")
        assert resp.status == 200
        assert CAR_DATA["model"] in await resp.text()

    @unittest_run_loop
    async def test_create_car_view(self):

        resp = await self.client.post("/create", data=CAR_DATA)
        assert resp.status == 200

        car = await Car.find_one({})
        assert car.vin_code == CAR_DATA["vin_code"]

    @unittest_run_loop
    async def test_update_car_view(self):
        await create_car(CAR_DATA)
        car = await Car.find_one({})
        edit_data = {"manufacturer": "Toyota"}
        resp = await self.client.post(f"{car.id}/update", data=edit_data)
        assert resp.status == 200

        updated_car = await Car.find_one({})
        assert car.manufacturer != updated_car.manufacturer

    @unittest_run_loop
    async def test_delete_car_view(self):
        await create_car(CAR_DATA)
        car = await Car.find_one({})

        resp = await self.client.get(f"{car.id}/delete")
        assert resp.status == 200

        deleted_car = await Car.find_one({})
        assert car != deleted_car
