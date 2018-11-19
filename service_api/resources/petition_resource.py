import hashlib
import uuid
from aiopg.sa import create_engine
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json as sanic_json

from service_api.schemas import PetitionPostSchema, PetitionPutSchema
from marshmallow import ValidationError
from service_api.models.petition import Petition
from database import dsn
from psycopg2 import IntegrityError


class PetitionResource(HTTPMethodView):

    post_schema = PetitionPostSchema()
    put_schema = PetitionPutSchema()

    def __init__(self):
        pass

    async def post(self, request: Request):

        headers = request.headers

        if not headers.get("X-User", None):
            return sanic_json("No user in headers", 401)

        if request.app.TOKEN_CACHE.get(headers.get("X-User"), None):
            user_id = headers.get("X-User")

        else:
            return sanic_json("No active user found", 401)

        try:
            args = self.post_schema.load(request.json)

        except ValidationError:
            return sanic_json("Incorrect arguments", 400)

        try:
            async with create_engine(dsn) as engine:
                async with engine.acquire() as conn:
                    args["user_id"] = request.app.TOKEN_CACHE.get(headers.get("X-User"))
                    await Petition.insert(conn, args)

        except IntegrityError:
            return sanic_json("Such user already exists", 406)

        return sanic_json("SUCCESS", 200)

    async def get(self, request: Request, petition_id: str = None):

        if petition_id:

            async with create_engine(dsn) as engine:
                async with engine.acquire() as conn:
                    result = await Petition.select(conn, petition_id)

                    # User logged in
                    if result:
                        return sanic_json(result, 200)

                    else:
                        return sanic_json(None, 400)

        else:
            async with create_engine(dsn) as engine:
                async with engine.acquire() as conn:
                    result = await Petition.select(conn)

                    # User logged in
                    if result:
                        return sanic_json(result, 200)

                    else:
                        return sanic_json(None, 400)

    async def put(self, request: Request, petition_id: str = None):

        headers = request.headers

        if not petition_id:
            return sanic_json("No id provided", 404)

        if not headers.get("X-User", None):
            return sanic_json("No user in headers", 401)

        if request.app.TOKEN_CACHE.get(headers.get("X-User"), None):
            user_id = headers.get("X-User")

        else:
            return sanic_json("No active user found", 401)

        try:
            args = self.put_schema.load(request.json)

        except ValidationError:
            return sanic_json("Incorrect arguments", 400)

        try:
            async with create_engine(dsn) as engine:
                async with engine.acquire() as conn:
                    args["user_id"] = request.app.TOKEN_CACHE.get(headers.get("X-User"))
                    await Petition.update(conn, petition_id, args)

            return sanic_json("SUCCESS", 200)

        except Exception:
            return sanic_json("Something went wrong", 500)

    async def delete(self, request: Request, petition_id: str = None):

        headers = request.headers

        if not petition_id:
            return sanic_json("No id provided", 404)

        if not headers.get("X-User", None):
            return sanic_json("No user in headers", 401)

        if request.app.TOKEN_CACHE.get(headers.get("X-User"), None):
            user_id = headers.get("X-User")

        else:
            return sanic_json("No active user found", 401)

        try:
            async with create_engine(dsn) as engine:
                async with engine.acquire() as conn:
                    await Petition.delete(conn, petition_id)

            return sanic_json("SUCCESS", 200)

        except Exception:
            return sanic_json("Something went wrong", 500)