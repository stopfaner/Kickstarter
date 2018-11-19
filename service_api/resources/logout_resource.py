from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json as sanic_json


class LogoutResource(HTTPMethodView):

    def __init__(self):
        pass

    async def post(self, request: Request):

        headers = request.headers
        if headers.get("X-User", None):

            access_token = headers.get("X-User")

            if access_token in request.app.TOKEN_CACHE:
                request.app.TOKEN_CACHE.pop(access_token)

                return sanic_json("SUCCESS", 200)

            else:

                return sanic_json("No user with this token", 201)
        else:
            return sanic_json("No user header passed", 201)


