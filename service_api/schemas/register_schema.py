from marshmallow import Schema, EXCLUDE, validates, ValidationError
from marshmallow.fields import Email, String


class RegisterSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    first_name = String(required=True, allow_none=False)
    last_name = String(required=False, allow_none=False)
    email = Email(required=True, allow_none=False)
    password = String(required=True, allow_none=False)

    @validates("password")
    def password_validation(self, password):

        if len(password) > 16 or len(password) < 8:
            raise ValidationError("Password must be 8-16 characters length")
