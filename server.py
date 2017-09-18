"""Server for accessing REDIS."""
import asyncio
from aiohttp import web
from src.redis import RedisAIO
import src.auxil as auxil
import logging

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


def set_routes(app):
    """Set all routes of pyRedisManager."""
    app.router.add_post(PATH_LOGIN, login_handler)
    app.router.add_post(PATH_CMD, commands_handler)


async def main(loop):
    """Main."""
    # instantiate REDIS:
    global redis
    redis = RedisAIO()
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
    # setup other stuff on web server:
    set_routes(app)
    app.on_shutdown.append(on_shutdown)
    # run the app:
    web.run_app(app, host="localhost", port=5000)
