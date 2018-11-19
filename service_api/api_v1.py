from sanic import Blueprint
from sanic.app import Sanic
from service_api.resources import *


api_prefix = "/kickstarter/v1"
uuid_regex = "[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}"


def load_api(app: Sanic):
    api_v1 = Blueprint("v1", url_prefix=api_prefix)

    api_v1.add_route(RegisterResource.as_view(), "/register")
    api_v1.add_route(LoginResource.as_view(), "/login")
    api_v1.add_route(LogoutResource.as_view(), "/logout")
    api_v1.add_route(UserResource.as_view(), f"/user/<user_id:{uuid_regex}>")

    api_v1.add_route(PetitionResource.as_view(), "/petition")
    api_v1.add_route(PetitionResource.as_view(), f"/petition/<petition_id:{uuid_regex}>")

    app.blueprint(api_v1)
