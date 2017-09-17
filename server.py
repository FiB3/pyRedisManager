""""""
import asyncio
from aiohttp import web
from src.redis import RedisAIO
import src.auxil as auxil


PATH_LOGIN = "/api/login"
"""Path for logging in."""
PATH_CMD = "/api/commands"
"""Path for running commands in REDIS."""
JWT_PROTECTED_PATHS = [PATH_CMD]
"""List of paths, that must be protected by JWT."""


async def login_middleware(app, handler):
    async def middleware_handler(request):
        """Middleware for JWT check."""
        pass

    return middleware_handler


async def login_handler(request):
    """Handler for user login - gets a JWT token."""
    pass


async def commands_handler(request):
    """Handler, which runs a single command in REDIS."""
    pass


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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print("test")
    # instantiate web.Application:
    app = web.Application()  # TODO: add middleware
    # setup routes:
    set_routes(app)
    # TODO: add on_shutdown

    # run the app:
    web.run_app(app)
