"""Server for accessing REDIS."""
import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2
import logging
# my modules:
from src.redis import RedisAIO
import src.auxil as auxil

OS_PATH_TO_TEMPLATES = "./templates/"

PATH_LOGIN_UI = "/login"
"""Path for obtaining web interface in REDIS."""
PATH_CMD_UI = "/interface"
"""Path for obtaining web interface in REDIS."""

PATH_LOGIN = "/api/login"
"""Path for logging in."""
PATH_CMD = "/api/commands"
"""Path for running commands in REDIS."""

JWT_PROTECTED_PATHS = [PATH_CMD, PATH_CMD_UI]
"""List of paths, that must be protected by JWT."""


async def login_middleware(app, handler):
    """Middleware for JWT check."""
    async def middleware_handler(request):
        """Middleware for JWT check."""
        return await handler(request)

    return middleware_handler


async def login_handler(request):
    """Handler for user login - gets a JWT token."""
    pass


async def commands_handler(request):
    """Handler, which runs a single command in REDIS."""
    cmd = await request.text()

    res = await redis.run_cmd(cmd)

    return web.Response(text=res)


async def login_ui_handler(request):
    """Handler for user login - gets a JWT token."""
    pass


@aiohttp_jinja2.template("interface.html")
async def commands_ui_handler(request):
    """Handler, which runs a single command in REDIS."""

    return {}


def set_routes(app):
    """Set all routes of pyRedisManager."""
    # prep API routes:
    app.router.add_post(PATH_LOGIN, login_handler)
    app.router.add_post(PATH_CMD, commands_handler)
    # prep web pages routes
    app.router.add_get(PATH_LOGIN_UI, login_ui_handler)
    app.router.add_get(PATH_CMD_UI, commands_ui_handler)


async def main(loop):
    """Main."""
    # instantiate REDIS:
    redis_info = auxil.get_redis_info()  # get info about redis as a list
    global redis
    redis = RedisAIO(*redis_info)
    await redis.connect()


async def on_shutdown(app):
    """Gracefully kill the server."""
    # TODO: close login coroutines, if needed:

    # close REDIS:
    await redis.close()


if __name__ == '__main__':
    # Set up logging:
    logging.basicConfig(level=logging.DEBUG)
    # Prepare async loop:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    # instantiate web.Application:
    app = web.Application(middlewares=[login_middleware])
    # add jinja2 into the server:
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(OS_PATH_TO_TEMPLATES))
    # setup other stuff on web server:
    set_routes(app)
    app.on_shutdown.append(on_shutdown)
    # run the app:
    server_info = auxil.get_server_info_on_local()
    web.run_app(app, host=server_info["host"], port=server_info["port"])
