import hashlib
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json as sanic_json
from service_api.schemas import RegisterSchema
from marshmallow import ValidationError
from aiopg.sa import create_engine

from database import dsn
from service_api.models.user import User
from psycopg2 import IntegrityError


class RegisterResource(HTTPMethodView):

    post_schema = RegisterSchema()

    def __init__(self):
        pass

    async def post(self, request: Request):

        try:
            args = self.post_schema.load(request.json)
        except ValidationError as err:
            return sanic_json(err.messages, 400)

        args["password"] = hashlib.sha224(args["password"].encode()).hexdigest()

        try:
            async with create_engine(dsn) as engine:
                async with engine.acquire() as conn:
                    await User.insert(conn, args)

        except IntegrityError:
            return sanic_json("Such user already exists", 406)

        return sanic_json("Success", 201)
