import hashlib
import uuid
from aiopg.sa import create_engine
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json as sanic_json

from service_api.schemas import LoginSchema
from marshmallow import ValidationError
from service_api.models.user import User
from database import dsn


class LoginResource(HTTPMethodView):

    login_schema = LoginSchema()

    def __init__(self):
        pass

    async def post(self, request: Request):

        try:
            args = self.login_schema.load(request.json)

        except ValidationError:
            return sanic_json("Incorrect arguments", 400)

        args["password"] = hashlib.sha224(args["password"].encode()).hexdigest()

        async with create_engine(dsn) as engine:
            async with engine.acquire() as conn:
                result = await User.login(conn, args)

                # User logged in
                if result:
                    token = str(uuid.uuid4())
                    request.app.TOKEN_CACHE[token] = result["id"]

                    return sanic_json({
                        "access_token": token
                    }, 200)

                else:
                    return sanic_json("FAILURE", 400)
