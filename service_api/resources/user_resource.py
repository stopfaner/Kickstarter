from aiopg.sa import create_engine
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json as sanic_json

from service_api.models.user import User
from database import dsn


class UserResource(HTTPMethodView):

    async def get(self, request: Request, user_id: str = None):

        if not user_id:
            return sanic_json("No id specified", 404)

        async with create_engine(dsn) as engine:
            async with engine.acquire() as conn:
                result = await User.select(conn, user_id)

                # User logged in
                if result:
                    result.pop("password")
                    result["id"] = str(result["id"])

                    return sanic_json(result, 200)

                else:
                    return sanic_json({}, 400)
