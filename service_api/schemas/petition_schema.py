
from marshmallow import Schema, EXCLUDE
from marshmallow.fields import String, Float, Integer


class PetitionPostSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    petition_name = String(required=True, allow_none=False)

    petition_description = String(required=True)

    petition_current_money = Float(required=True)

    petition_current_like = Integer(required=True)

    image_url = String(required=False)


class PetitionPutSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    petition_name = String(required=False, allow_none=False)

    petition_description = String(required=False, allow_none=False)

    petition_current_money = Float(required=False, allow_none=False)

    petition_current_like = Integer(required=False, allow_none=False)

    image_url = String(required=False, allow_none=False)
