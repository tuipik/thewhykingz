from views import (
    index,
    create_car,
    car_detail,
    update_car,
    update_car_apply,
    delete_car,
)


def setup_routes(app):
    app.router.add_get("/", index, name="index")
    app.router.add_get("/create", create_car, name="create-car")
    app.router.add_post("/create", create_car, name="create-car")
    app.router.add_get(f"/{{car_id}}", car_detail, name="car-detail")
    app.router.add_get(f"/{{car_id}}/update", update_car, name="update-car")
    app.router.add_post(
        f"/{{car_id}}/update", update_car_apply, name="update-car-apply"
    )
    app.router.add_get(f"/{{car_id}}/delete", delete_car, name="delete-car")
