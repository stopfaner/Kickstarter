from marshmallow import Schema, EXCLUDE, validates, ValidationError
from marshmallow.fields import Email, String


class LoginSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    email = Email(required=True, allow_none=False)
    password = String(required=True, allow_none=False)
