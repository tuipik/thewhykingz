import datetime
from marshmallow import Schema, fields, validate, pre_load


CURRENT_YEAR = datetime.datetime.now().year
VIN_CODE_REGEX = r"[a-zA-Z0-9]{9}[a-zA-Z0-9]{2}[0-9]{6}"


class CarSchema(Schema):
    model = fields.String(required=True)
    manufacturer = fields.String(required=True)
    release_year = fields.Integer(
        required=True, validate=validate.Range(min=1900, max=CURRENT_YEAR)
    )
    colour = fields.String(required=True)
    vin_code = fields.String(
        required=True,
        validate=validate.Regexp(VIN_CODE_REGEX),
    )
    created_time = fields.DateTime(dump_only=True)
    updated_time = fields.DateTime(dump_only=True)

    @pre_load
    def manufacturer_in_lower_case(self, data):
        try:
            data["manufacturer"] = data["manufacturer"].lower()
        except KeyError:
            pass
        return data


class UpdateCarSchema(CarSchema):
    class Meta:
        fields = ["model", "manufacturer", "release_year", "colour", "vin_code"]
