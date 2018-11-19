import asyncio
from sanic import Sanic
from sanic_cors import CORS
from service_api import api_v1


app = Sanic(__name__)
app.TOKEN_CACHE = dict()

CORS(
    app,
    resources={r"*": {"origins": "*"}},
    expose_headers=[
        "link"
    ],
)

api_v1.load_api(app)


def request_task_factory(loop, coro):
    """ Task factory that provide request object inheritance for child tasks.  """
    child_task = asyncio.tasks.Task(coro, loop=loop)
    parent_task = asyncio.Task.current_task(loop=loop)
    current_request = getattr(parent_task, 'request', None)
    setattr(child_task, 'request', current_request)

    return child_task


@app.listener('before_server_start')
async def init(_, loop):
    """ Set task factory for request object inheritance. """
    loop.set_task_factory(request_task_factory)

if __name__ == "__main__":
    app.run(port=4000)
